# Multi-Functional-AI-Assistant
This is a multifunctional AI assistant that uses DialoGPT model which was trained on 735 million reddit posts. It is capable of answering to almost all kind of questions and it can also be fine tuned in case you want to increase the temperature of the model or train it on new data and give it a personality. For natural language processing (NLP), NVIDIA's RIVA model was used. This is one of the fastest and most accurate models out there and it is fully customizable. The model offers Automatic Speech Recognition (ASR), Text-to_Speech (TTS) and a lot more. RIVA can be only installed in Linux operating system, so if you are using Windows as your operating system, you might use Pyaudio library instead. The AI assistant is also capable of making object detections of 96 different objects and say the names of the objects it sees in real time. Some of these are listed below. To turn on the object detection feature, all you have to do is to say "object detection" in a sentance. Finally, the AI assistant uses multiple APIs from different sources to answer some of the most common questions that people might ask, do some of the basic tasks that people do daily and to give most updated answers to those questions. Some of these task are sending an email or a WhatsApp message, do Google, Wkipedia search etc. The list of the APIs used in this project are listed below.

![demo1](https://user-images.githubusercontent.com/111835151/186729682-6301b5df-6732-495e-9155-fb066f453c29.gif)

## Requirements
- Linux operating system
- CUDA capable GPU with **minimum** of 12 GB RAM
- CUDA Toolkit
- DialoGPT Model
- NVIDIA RIVA
- Camera (Webcam)

**NOTE: Each of the items listed above has their own requirements.**

## List of APIs
| API | ACTIVATE |
| --- | --- |
| Search on Youtube | "Youtube" |
| Search on Google | "search on google" |
| Search on Wkipedia | "Youtube" |
| Weather information | "Youtube" |
| Currency Conversion | "Youtube" |

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
