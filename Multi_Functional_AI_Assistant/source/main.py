from ipaddress import ip_address
from locale import currency
from random import choice
from threading import Thread
import threading
import requests
from riva_engine.riva_stt import Riva_Listen, greet_user
from riva_engine.riva_stt import Riva_Speak
from operations.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_trending_movies, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message,get_currency
from operations.os_ops import open_calculator, open_camera, open_cmd, open_notepad
from pprint import pprint
from face_recognition.face_rec import start_face_rec
from object_detection.detect_obj import object_detection

filePath = "/home/jetno/Desktop/VSC/Advanced AI_Assistant/source/object_detection/file.txt"

def Start():

    greet_user()

    while True:
        query = Riva_Listen().lower()

        if "open notepad" in query:
            open_notepad()

        elif "open command prompt" in query or "open cmd" in query:
            open_cmd()

        elif "open camera" in query:
            open_camera()

        elif "open calculator" in query:
            open_calculator()

        elif "ip address" in query:
            ip_address = find_my_ip()
            Riva_Speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen.')
            print(f'Your IP Address is {ip_address}')

        elif "wikipedia" in query:
            Riva_Speak('what do you want to search on wikipedia?')
            search_query = Riva_Listen().lower()
            results = search_on_wikipedia(search_query)
            Riva_Speak(f"According to Wikipedia, {results}")
            Riva_Speak("For your convenience, I am printing it on the screen.")
            print(results)

        elif "youtube" in query:
            Riva_Speak('What do you want to play on Youtube?')
            video = Riva_Listen().lower()
            play_on_youtube(video)

        elif "search on google" in query:
            Riva_Speak('What do you want to search on Google?')
            query = Riva_Listen().lower()
            search_on_google(query)

        elif "send whatsapp message" in query:
            Riva_Speak('On what number should I send the message? Please enter in the console: ')
            number = input("Enter the number: ")
            Riva_Speak("What is the message?")
            message = Riva_Listen().lower()
            send_whatsapp_message(number, message)
            Riva_Speak("I've sent the message.")

        elif "send an email" in query:
            Riva_Speak("On what email address do I send? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            Riva_Speak("What should be the subject?")
            subject = Riva_Listen().capitalize()
            Riva_Speak("What is the message")
            message = Riva_Listen().capitalize()
            if send_email(receiver_address, subject, message):
                Riva_Speak("I've sent the email.")
            else:
                Riva_Speak("Something went wrong while I was sending the mail. Please check the error logs.")

        elif "joke" in query:
            Riva_Speak(f"Hmm, let me think.")
            joke = get_random_joke()
            Riva_Speak(joke)
            Riva_Speak("For your convenience, I am printing it on the screen.")
            pprint(joke)

        elif "advice" in query:
            Riva_Speak(f"Here's an advice for you.")
            advice = get_random_advice()
            Riva_Speak(advice)
            Riva_Speak("For your convenience, I am printing it on the screen.")
            pprint(advice)

        elif "trending movies" in query:
            Riva_Speak(f"Some of the trending movies are: {get_trending_movies()}")
            Riva_Speak("For your convenience, I am printing it on the screen.")
            print(*get_trending_movies(), sep='\n')

        elif "news" in query:
            Riva_Speak(f"I'm reading out the latest news headlines")
            Riva_Speak(get_latest_news())
            Riva_Speak("For your convenience, I am printing it on the screen.")
            print(*get_latest_news(), sep='\n')

        elif "weather" in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            Riva_Speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            Riva_Speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            Riva_Speak(f"Also, the weather report talks about {weather}")
            Riva_Speak("For your convenience, I am printing it on the screen.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")

        elif "convert currency" in query:
            Riva_Speak(f"what do we convert, please type")
            fr = input("From:")
            Riva_Speak("which currency do you want to convert to, please type")
            to = input("To: ")
            Riva_Speak("and what is the amount")
            amount = int(Riva_Listen())
            print("Recieved: {amount}")
            currency = get_currency(fr, to, amount)
            Riva_Speak(f'the currency is {currency}')
            Riva_Speak("I am printing out on the screen")
            print(currency)

        elif "face recognition" in query:
            Riva_Speak("For sure. Deploying face recognition library.")
            p1 = Thread(target=start_face_rec)
            p1.start()

        elif "object detection" in query:
            Riva_Speak("For sure, this will take a moment")
            p2 = Thread(target=object_detection)
            p2.start()
        
        elif 'what do you see' in query:
            with open(filePath, 'r') as f:
                namesOnList = f.read().splitlines()
                Riva_Speak(f"I see {namesOnList}")

###################################################################################################################################

if __name__ == "__main__":
    Start()
 

 
    
   
    
    
    
    
                