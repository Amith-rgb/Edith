import random
import pyttsx3
import requests
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import imdb
import pyautogui
import webbrowser
import gtts
from datetime import datetime
import wolframalpha
from decouple import config
from random import choice
from conv import random_text
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 2.5)
engine.setProperty('rate', 210)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Get the user and bot names from the environment variables
USER = config('USER')
BOT = config('BOT')


# Define a function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Define a function to greet the user
def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USER}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good Afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USER}")
    speak(f"I am {BOT}. How may I help you {USER}?")


# Define a function to start listening
def start_listening():
    global listening
    listening = True
    print("Start listening")


# Define a function to pause listening
def pause_listening():
    global listening
    listening = False
    print("Stop listening")


# Add hotkeys to start and pause listening
keyboard.add_hotkey('ctrl', start_listening)
keyboard.add_hotkey('alt', pause_listening)


# Define a function to take a command
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognising.......")
        queri = r.recognize_google(audio, language='en-in')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour <= 6:
                speak("Good night TakeCare")
            else:
                speak("Have a Good Day")
                exit()

    except Exception:
        speak("I couldn't hear you. Can you repeat it?")
        queri = 'None'
    return queri.lower()


# Define a function to process the query


# Main function
def main():
    greet_me()
    while True:
        query = take_command()
        process_query(query)


if __name__ == "__main__":
    def process_query(query):
        if "hi" in query:
            speak("I am good. What about you?")
        elif "how are you" in query:
            speak("I am fine sir. What about you?")
        elif "fine" in query:
            speak("does any task do have to do for you")
        elif "open command prompt" in query:
            speak("Opening command prompt")
            os.system('start cmd')
        elif "open camera" in query:
            speak("Opening camera")
            sp.run('start microsoft.windows.camara:', shell=True)
        elif "open notepad" in query:
            speak("Opening notepad")
            telegram_path = "C:\\Windows\\System32\\notepad.exe"
            os.system(telegram_path)
        elif "open vs code" in query:
            msi_path = "C:\\ProgramFiles\\Google\\Chrome\\Application\\chrome.exe"
            os.system(msi_path)
        elif "ip address" in query:
            ip_address = find_my_ip()
            speak(f"Your IP address is {ip_address}")
            print(f"Your IP address is {ip_address}")
        elif "open youtube" in query:
            speak("What do you want to play on YouTube?")
            video = take_command()
            youtube(video)
        elif "open google" in query:
            speak("What do you want to search on Google?")
            search = take_command()
            url = f"https://www.google.com/search?q={search}"
            webbrowser.get().open(url)
        elif "wikipedia" in query:
            speak("What do you want to search on Wikipedia?")
            search = take_command()
            results = search_on_wikipedia(search)
            speak(f"According to Wikipedia, {results}")
            speak("I am printing on terminal")
            print(results)
        elif "send email" in query:
            speak("On what email address do you want to send?")
            receiver_add = input("Email address: ")
            speak("What is the subject?")
            subject = take_command().capitalize()
            speak("What is the message?")
            message = take_command().capitalize()
            if '@' in receiver_add:
                send_email(receiver_add, subject, message)
            else:
                speak("Invalid email address")
        elif "news" in query:
            speak("What type of news do you want to hear?")
            topic = take_command()
            news = get_news(topic)
            speak(f"According to the news, {news}")
            speak("I am printing on terminal")
            print(news)
        elif "weather" in query:
            speak("What is your city name?")
            city = take_command()
            temp = weather(city)
            speak(f"The temperature in {city} is {temp} degree celcius")
            print(f"The temperature in {city} is {temp} degree celcius")
        elif "take a photo" in query:
            speak("Say cheese!")
            pic()
        elif "calculate" in query:
            speak("What do you want to calculate?")
            problem = take_command()
            print("Wait a second")
            answer = wolframalpha(problem)
            speak(f"The answer is {answer}")
        elif "who is" in query:
            speak("Who is the person you want to know about?")
            person = take_command()
            info = imdb(person)
            speak(f"According to IMDB, {info}")
            speak("I am printing on terminal")
            print(info)
        elif "what is" in query:
            speak("What do you want to know about?")
            thing = take_command()
            info = wolframalpha(thing)
            speak(f"According to Wolfram Alpha, {info}")
            speak("I am printing on terminal")
            print(info)
        elif "where is" in query:
            speak("What is the location you want to know about?")
            location = take_command()
            url = f"https://www.google.com/maps/place/{location}"
            webbrowser.get().open(url)
        elif "how to" in query:
            speak("What do you want to know how to do?")
            thing = take_command()
            url = f"https://www.google.com/search?q={thing}"
            webbrowser.get().open(url)
        elif "what is the time" in query:
            strTime = datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
        elif "what is the date" in query:
            strDate = datetime.now().strftime("%d %B %Y")
            speak(f"The date is {strDate}")
        elif "open" in query:
            speak("What do you want to open?")
            thing = take_command()
            url = f"https://www.google.com/search?q={thing}"
            webbrowser.get().open(url)
        elif "close" in query:
            speak("What do you want to close?")
            thing = take_command()
            pyautogui.press('esc')
        elif "play" in query:
            speak("What do you want to play?")
            thing = take_command()
            url = f"https://www.google.com/search?q={thing}"
            webbrowser.get().open(url)
        elif "search" in query:
            speak("What do you want to search?")
            thing = take_command()
            url = f"https://www.google.com/search?q={thing}"
            webbrowser.get().open(url)
        elif "find" in query:
            thing = take_command()
            url = f"https://www.google.com/search?q={thing}"
            webbrowser.get().open(url)
        elif "show" in query:
            speak("What do you want to show?")
            thing = take_command()
            url = f"https://www.google.com/search?q={thing}"
            webbrowser.get().open(url)
        elif "launch" in query:
            speak("What do you want to launch?")
            thing = take_command()
            url = f"https://www.google.com/search?q={thing}"
            webbrowser.get().open(url)
        elif "run" in query:
            speak("What do you want to run?")
            thing = take_command()
            url = f"https://www.google.com/search?q={thing}"
            webbrowser.get().open(url)
        elif "execute" in query:
            speak("What do you want to execute?")
            thing = take_command()
            url = f"https://www.google.com/search?q={thing}"
            webbrowser.get().open(url)
        elif "start" in query:
            speak("What do you want to start?")
            thing = take_command()
            url = f"https://www.google.com/search?q={thing}"
            webbrowser.get().open(url)
        elif "stop" in query or "exit" in query:
            speak("Goodbye")
            exit()
        else:
            speak("I didn't understand that. Can you please repeat it?")
            return


    main()
