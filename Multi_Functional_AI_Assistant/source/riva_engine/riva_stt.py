import argparse
import os
import queue
import sys
from threading import Thread
from time import sleep
import torch
import grpc
import pyaudio
from datetime import datetime
from decouple import config
import riva_api.riva_asr_pb2 as rasr
import riva_api.riva_asr_pb2_grpc as rasr_srv
import riva_api.riva_audio_pb2 as ra
from riva_engine.riva_tts import Riva_Speak
from riva_engine.flags import search_flag

from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-large")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-large")

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

USERNAME = config('USERNAME')
BOTNAME = config('BOTNAME')

def get_args():
    parser = argparse.ArgumentParser(description="Streaming transcription via Riva AI Services")
    parser.add_argument("--server", default="localhost:50051", type=str, help="URI to GRPC server endpoint")
    parser.add_argument("--input-device", type=int, default=None, help="output device to use")
    parser.add_argument("--list-devices", action="store_true", help="list output devices indices")
    parser.add_argument("--language-code", default="en-US", type=str, help="Language code of the model to be used")
    parser.add_argument("--ssl_cert", type=str, default="", help="Path to SSL client certificatates file")
    parser.add_argument(
        "--use_ssl", default=False, action='store_true', help="Boolean to control if SSL/TLS encryption should be used"
    )
    return parser.parse_args()


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk, device=None):
        self._rate = rate
        self._chunk = chunk
        self._device = device

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            input_device_index=self._device,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses):
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        partial_transcript = ""
        for result in response.results:
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript

            if not result.is_final:
                partial_transcript += transcript
            else:
                overwrite_chars = ' ' * (num_chars_printed - len(transcript))
                query = transcript + overwrite_chars
                print("## " + transcript + overwrite_chars + "\n")
                num_chars_printed = 0
                return query

        if partial_transcript != "":
            overwrite_chars = ' ' * (num_chars_printed - len(partial_transcript))
            sys.stdout.write(">> " + partial_transcript + overwrite_chars + '\r')
            sys.stdout.flush()
            num_chars_printed = len(partial_transcript) + 3

def greet_user():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        Riva_Speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        Riva_Speak(f"Good Afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        Riva_Speak(f"Good Evening {USERNAME}")
    Riva_Speak(f"I am {BOTNAME}. How may I asist you?")

def Riva_Listen():
    args = get_args()

    if args.list_devices:
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] < 1:
                continue
            print(f"{info['index']}: {info['name']}")
        sys.exit(0)

    if args.ssl_cert != "" or args.use_ssl:
        root_certificates = None
        if args.ssl_cert != "" and os.path.exists(args.ssl_cert):
            with open(args.ssl_cert, 'rb') as f:
                root_certificates = f.read()
        creds = grpc.ssl_channel_credentials(root_certificates)
        channel = grpc.secure_channel(args.server, creds)
    else:
        channel = grpc.insecure_channel(args.server)

    client = rasr_srv.RivaSpeechRecognitionStub(channel)

    config = rasr.RecognitionConfig(
        encoding=ra.AudioEncoding.LINEAR_PCM,
        sample_rate_hertz=RATE,
        language_code=args.language_code,
        max_alternatives=1,
        enable_automatic_punctuation=True,
    )
    streaming_config = rasr.StreamingRecognitionConfig(config=config, interim_results=True)

    with MicrophoneStream(RATE, CHUNK, device=args.input_device) as stream:
        audio_generator = stream.generator()
        requests = (rasr.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)

        def build_generator(cfg, gen):
            yield rasr.StreamingRecognizeRequest(streaming_config=cfg)
            for x in gen:
                yield x

        responses = client.StreamingRecognize(build_generator(streaming_config, requests))
        queryInput = listen_print_loop(responses)

        flag = search_flag(queryInput)
        if flag == False:
            for step in range(1):
                new_user_input_ids = tokenizer.encode(f"{queryInput}" + tokenizer.eos_token, return_tensors='pt')
                bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids
                chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
                Riva_Speak("{}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))
        
    return queryInput


