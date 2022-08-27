import argparse
import os
import sys
import time
import wave

import grpc
import numpy as np
import pyaudio
import riva_api.riva_audio_pb2 as ra
import riva_api.riva_tts_pb2 as rtts
import riva_api.riva_tts_pb2_grpc as rtts_srv


def get_args():
    parser = argparse.ArgumentParser(description="Streaming transcription via Riva AI Services")
    parser.add_argument("--server", default="localhost:50051", type=str, help="URI to GRPC server endpoint")
    parser.add_argument("--voice", type=str, help="voice name to use", default="English-US-Female-1")
    parser.add_argument("-o", "--output", default=0, type=str, help="Output file to write last utterance")
    parser.add_argument("--list-devices", action="store_true", help="list output devices indices")
    parser.add_argument("--output-device", type=int, help="Output device to use")
    parser.add_argument("--ssl_cert", type=str, default="", help="Path to SSL client certificatates file")
    parser.add_argument(
        "--use_ssl", default=False, action='store_true', help="Boolean to control if SSL/TLS encryption should be used"
    )
    return parser.parse_args()

def Riva_Speak(queryInput):
    args = get_args()

    if args.ssl_cert != "" or args.use_ssl:
        root_certificates = None
        if args.ssl_cert != "" and os.path.exists(args.ssl_cert):
            with open(args.ssl_cert, 'rb') as f:
                root_certificates = f.read()
        creds = grpc.ssl_channel_credentials(root_certificates)
        channel = grpc.secure_channel(args.server, creds)
    else:
        channel = grpc.insecure_channel(args.server)

    tts_client = rtts_srv.RivaSpeechSynthesisStub(channel)
    audio_handle = pyaudio.PyAudio()

    if args.list_devices:
        for i in range(audio_handle.get_device_count()):
            info = audio_handle.get_device_info_by_index(i)
            if info['maxOutputChannels'] < 1:
                continue
            print(f"{info['index']}: {info['name']}")
        sys.exit(0)

    req = rtts.SynthesizeSpeechRequest()
    req.text = "Hello"
    req.language_code = "en-US"
    req.encoding = ra.AudioEncoding.LINEAR_PCM
    req.sample_rate_hz = 44100
    req.voice_name = args.voice

    stream = audio_handle.open(
        format=pyaudio.paInt16,
        output_device_index=args.output_device,
        channels=1,
        rate=req.sample_rate_hz,
        output=True,
    )
    
    print("Speak: ", end='')
    req.text = str(queryInput)
    if args.output:
        wav = wave.open(args.output, 'wb')
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(req.sample_rate_hz)

    print("Generating audio for request...")
    print(f"  > '{req.text}': ", end='')
    start = time.time()
    resp = tts_client.Synthesize(req)
    stop = time.time()
    print(f"Time to first audio: {(stop-start):.3f}s")
    stream.write(resp.audio)
    if args.output:
        wav.writeframesraw(resp.audio)
        wav.close()
