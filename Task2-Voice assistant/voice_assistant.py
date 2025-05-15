# ---------------------------------------------
# Imports and Initialization
# ---------------------------------------------
import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import speech_recognition as sr
from datetime import datetime, timedelta
import webbrowser
import smtplib
from email.mime.text import MIMEText
import requests
import time
import pywhatkit
import pyjokes

# Text-to-speech engine
engine = pyttsx3.init()

# ---------------------------------------------
# Core Functionalities
# ---------------------------------------------
def speak(text, display_callback=None):
    if display_callback:
        display_callback(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command(display_callback=None):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        if display_callback:
            display_callback("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        if display_callback:
            display_callback("Recognizing...")
        command = recognizer.recognize_google(audio)
        if display_callback:
            display_callback(f"You: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.", display_callback)
        return ""
    except sr.RequestError:
        speak("Sorry, I am having trouble connecting to the internet.", display_callback)
        return ""

def wish_user(display_callback=None):
    hour = datetime.now().hour
    if hour < 12:
        speak("Good morning!", display_callback)
    elif hour < 18:
        speak("Good afternoon!", display_callback)
    else:
        speak("Good evening!", display_callback)
    speak("I am your voice assistant. How can I help you today?", display_callback)

# ---------------------------------------------
# Email Functionality
# ---------------------------------------------
def send_email(recipient, subject, body, display_callback=None):
    sender_email = "your_email@gmail.com"
    password = "your_password"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, recipient, msg.as_string())
        speak("Email sent successfully.", display_callback)
    except Exception as e:
        speak("Sorry, I could not send the email.", display_callback)
        print(e)

# ---------------------------------------------
# Weather Functionality
# ---------------------------------------------
def get_weather(city, display_callback=None):
    api_key = "your_api_key"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(complete_url)
        data = response.json()
        if data["cod"] == "404":
            speak("City not found.", display_callback)
        else:
            main = data["main"]
            weather = data["weather"][0]["description"]
            temp = main["temp"]
            speak(f"The weather in {city} is {weather} with a temperature of {temp}°C.", display_callback)
    except Exception as e:
        speak("Sorry, I couldn't fetch the weather information.", display_callback)
        print(e)

# ---------------------------------------------
# Reminder Functionality
# ---------------------------------------------
def set_reminder(reminder_time, message, display_callback=None):
    try:
        reminder_dt = datetime.strptime(reminder_time, "%H:%M")
        now = datetime.now()
        reminder_dt = reminder_dt.replace(year=now.year, month=now.month, day=now.day)
        if reminder_dt < now:
            reminder_dt += timedelta(days=1)
        while datetime.now() < reminder_dt:
            time.sleep(10)
        speak(f"Reminder: {message}", display_callback)
    except ValueError:
        speak("Invalid time format. Use HH:MM.", display_callback)

# ---------------------------------------------
# Voice Command Processor
# ---------------------------------------------
def process_command(display_callback):
    command = take_command(display_callback)
    if not command:
        return
    if "hello" in command:
        speak("Hello! Nice to meet you.", display_callback)
    elif "time" in command:
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.", display_callback)
    elif "date" in command:
        today = datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {today}.", display_callback)
    elif "search" in command:
        speak("What do you want to search for?", display_callback)
        query = take_command(display_callback)
        if query:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            speak(f"Here are the search results for {query}.", display_callback)
    elif "send email" in command:
        speak("Who do you want to send an email to?", display_callback)
        recipient = take_command(display_callback)
        speak("What is the subject of the email?", display_callback)
        subject = take_command(display_callback)
        speak("What is the body of the email?", display_callback)
        body = take_command(display_callback)
        send_email(recipient, subject, body, display_callback)
    elif "weather" in command:
        speak("Which city's weather do you want to know?", display_callback)
        city = take_command(display_callback)
        get_weather(city, display_callback)
    elif "set reminder" in command:
        speak("At what time should I remind you? Say it in HH:MM format.", display_callback)
        reminder_time = take_command(display_callback)
        speak("What should I remind you about?", display_callback)
        message = take_command(display_callback)
        set_reminder(reminder_time, message, display_callback)
    elif "play song" in command:
        speak("What song would you like to hear?", display_callback)
        song = take_command(display_callback)
        pywhatkit.playonyt(song)
        speak(f"Playing {song} on YouTube.", display_callback)
    elif "tell me a joke" in command:
        joke = pyjokes.get_joke()
        speak(joke, display_callback)
    elif "stop" in command or "exit" in command:
        speak("Goodbye! Have a nice day.", display_callback)
        exit()
    else:
        speak("I am not sure how to help with that.", display_callback)

# ---------------------------------------------
# GUI Setup and Interaction
# ---------------------------------------------
def display_callback(message):
    chat_log.insert(tk.END, f"{message}\n")
    chat_log.see(tk.END)

def start_listening():
    process_command(display_callback)

# GUI Window Configuration
root = tk.Tk()
root.title("Voice Assistant")
root.geometry("600x400")

chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

start_button = tk.Button(root, text="Start Listening", font=("Arial", 14), command=start_listening)
start_button.pack(pady=10)

# ---------------------------------------------
# Start Assistant
# ---------------------------------------------
wish_user(display_callback)
root.mainloop()
