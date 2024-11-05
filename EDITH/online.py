import random
import PIL.Image
import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
import PIL.Image
from decouple import config

EMAIL = ""                         """enter the email address"""
PASSWORD = ""                       """enter the password"""


def find_my_ip():
    ip_address = requests.get('https://api.ipify.org?format=json').json()
    return ip_address["ip"]


def search_on_wikipedia(queri):
    results = wikipedia.summary(queri, sentences=2)
    return results


def search_on_google(queri):
    kit.search(queri)


def youtube(video):
    kit.playonyt(video)


def send_email(receiver_add, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_add
        email['subject'] = subject
        email['from'] = EMAIL

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


def get_news():
    news_headline = []
    api_key = 'a99f1461e5cb4be787f3d677a26fadc7'                                        """Replace with your API key"""
    url = f"https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey=a99f1461e5cb4be787f3d677a26fadc7"
    response = requests.get(url)

    if response.status_code == 200:
        result = response.json()
        print("API response:", result)
        articles = result["articles"]
        for article in articles:
            news_headline.append(article["title"])
        return news_headline[:6]


def weather(city):
    res = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=a27b99456fd7da2b22edf857ecd9ca2b"
    ).json()
    weather = res["weather"][0]["main"]
    temp = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temp}°C", f"{feels_like}°C"



