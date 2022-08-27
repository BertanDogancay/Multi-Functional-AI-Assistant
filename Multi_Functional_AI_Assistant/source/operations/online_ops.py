from ipaddress import ip_address
from random import choice
import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

{
  "ip": "117.214.111.199"
}

def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]

def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

def play_on_youtube(video):
    kit.playonyt(video)

def search_on_google(query):
    kit.search(query)

def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+90{number}", message)

EMAIL = config("EMAIL")
PASSWORD = config("PASSWORD")

def send_email(reciever_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = reciever_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False

NEWS_API_KEY = config("NEWS_API_KEY")
def get_latest_news():
    news_headlines = []
    res = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res["articles"]
    for article in articles:
        news_headlines.append(article["title"])
    return news_headlines[:5]

OPEN_WEATHER_APP_ID = config("OPEN_WEATHER_APP_ID")
def get_weather_report(city):
    res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPEN_WEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"

TMDB_API_KEY = config("TMDB_API_KEY")
def get_trending_movies():
    trending_movies = []
    res = requests.get(f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]

XRAPID_API_HOST = config("XRAPID_API_HOST_CURRENCY")
XRAPID_API_KEY = config("XRAPID_API_KEY_CURRENCY")
def get_currency(fr, to, amount):
    url = "https://currency-converter-by-api-ninjas.p.rapidapi.com/v1/convertcurrency"
    querystring = {"have":{fr},"want":{to},"amount":{amount}}
    headers = {
        'x-rapid-api-host': XRAPID_API_HOST,
        'x-rapidapi-key': XRAPID_API_KEY
    }
    response = requests.request("GET", url, headers=headers, params=querystring).json()
    return response["new_amount"]

def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]

def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']

