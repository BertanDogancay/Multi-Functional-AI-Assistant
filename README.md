# Multi-Functional-AI-Assistant
An advanced AI assistant that can make object detections and uses dialogpt model, Nvidia RIVA for NLP, TTS, STT and multiple APIs from more than 10 different sources.

## Preface:
Before going any further, this project is not meant to be a real application due to the amout of gpu power it requires and the veraity of sources it needs to be able to work. If you like to explore, test this kind of stuff and have fun while doing it, then this project will be a great start for you. There is a lot of room to improve, you can even give it a UI and use it on your own computer.

## Requirements:
- Linux operating system
- CUDA capable GPU with **minimum** of 12 GB RAM
- CUDA Toolkit
- DialoGPT Model
- NVIDIA RIVA
- Camera (Webcam)

**NOTE: Each of the items listed above has their own requirements.**

This multifunctional AI assistant uses DialoGPT model which was trained on 735 million reddit posts. It is capable of answering to almost all kind of questions and it can also be fine tuned in case you want to increase the temperature of the model or train it on new data and give it a personality. For natural language processing (NLP), NVIDIA's RIVA model was used. This model is one of the fastest and most accurate models out there and it is fully customizable. The model offers Automatic Speech Recognition (ASR), Text-to_Speech (TTS) and a lot more. RIVA can only be installed on Linux operating system, so if you are using Windows as your operating system, you might use Pyaudio library instead. 

![demo1](https://user-images.githubusercontent.com/111835151/186729682-6301b5df-6732-495e-9155-fb066f453c29.gif)

The AI assistant is capable of making object detections of 96 different objects and say the names of the objects it sees in real time. Some of these are listed below. To activate the object detection feature, all you have to do is to say "object detection" in a sentance. Due to the use of multiprocessing, the user will still be able to have a conversation with the assistant or use the APIs while the camera is on and making object detections. The AI assistant has also face recognition feature, but there is still lot to improve in that area, so it's not recommended to be used yet.

<table>
  <thead>
    <th>Pose 1</th>
    <th>Pose 2</th>
  </thead>
  <tbody>
    <tr>
      <td> <img src="https://user-images.githubusercontent.com/111835151/186730713-cc276288-d72f-4a53-b9de-fc9d09f7c586.png"></td>
      <td> <img src="https://user-images.githubusercontent.com/111835151/186730774-26782fa0-525e-4779-9953-3c48c183dfaf.png"></td>
    </tr>
  </tbody>
</table>

Finally, the AI assistant uses multiple APIs from different sources to answer some of the most common questions that people might ask and do some of the basic tasks that people do daily. Some of these tasks are sending an email or a WhatsApp message, do Google, Wikipedia search etc. The list of the APIs used in this project are also listed below.

## List of APIs:
| API | ACTIVATE |
| --- | --- |
| Search on Youtube | "youtube" |
| Search on Google | "search on google" |
| Search on Wikipedia | "wikipedia" |
| Weather information | "weather" |
| Currency Conversion | "convert currency" |
| Notepad | "open notepad" |
| Command Prompt | "open cmd" "open command prompt" |
| Calculator | "open calculator" |
| Ip Address | "ip address" |
| WhatsApp Message | "send whatsapp message" |
| Email | "send an email" |
| Joke | "joke" |
| Advice | "advice" |
| Trending Movies | "trending movies" |
| Up to Date News | "news" |

| FEATURE | ACTIVATE |
| --- | --- |
| Face Recognition | "face recognition" |
| Object Detection | "object detection" |

<table>
  <tbody>
    <tr>
      <td> <img src="https://user-images.githubusercontent.com/111835151/186786136-27124ce6-5870-4a54-91fd-34d4b2e5e1f0.gif"></td>
    </tr>
    <tr>
      <td> <img src="https://user-images.githubusercontent.com/111835151/186786302-68505599-5220-4d02-9885-67b16535e7b7.gif"></td>
    </tr>
  </tbody>
</table>
