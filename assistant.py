import speech_recognition as sr
import pyttsx3
import requests
import threading
import pyttsx3
import requests
from memory import load_memory, save_memory

memory = load_memory()


def ask_ai(prompt):

    global memory

    memory.append({"role":"user","content":prompt})

    context = ""

    for item in memory[-10:]:

        context += item["role"] + ": " + item["content"] + "\n"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model":"llama3",
            "prompt": context + "assistant:",
            "stream":False
        }
    )

    reply = response.json()["response"]

    memory.append({"role":"assistant","content":reply})

    save_memory(memory)

    return reply
engine = pyttsx3.init()

voices = engine.getProperty('voices')

# female voice (usually index 1 on Windows)
engine.setProperty('voice', voices[1].id)

engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)


def speak(text):

    engine.stop()

    engine.say(text)

    engine.runAndWait()

from memory import load_memory, save_memory
from app_launcher import open_app
from system_control import type_text, press_key, open_search
from reminder import reminder_timer
from vision import read_screen_text
from screen_control import click_image


engine = pyttsx3.init()

memory = load_memory()

speaking = False


def speak(text):

    global speaking

    print("ROS:", text)

    speaking = True

    engine.say(text)

    engine.runAndWait()

    speaking = False


def stop_speaking():

    global speaking

    engine.stop()

    speaking = False


def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio).lower()

        print("You:", text)

        return text

    except:

        return ""


def ask_ai(prompt):

    global memory

    memory.append({"role":"user","content":prompt})

    context = ""

    for item in memory[-10:]:
        context += item["role"] + ": " + item["content"] + "\n"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model":"llama3",
            "prompt": context + "assistant:",
            "stream":False
        }
    )

    reply = response.json()["response"]

    memory.append({"role":"assistant","content":reply})

    save_memory(memory)

    return reply


def run_assistant():

    while True:

        command = listen()

        if command == "":
            continue


        # stop speaking

        if "stop talking" in command:

            stop_speaking()

            continue


        # open apps

        if command.startswith("open"):

            app = command.replace("open", "").strip()

            response = open_app(app)

            speak(response)

            continue


        # typing automation

        if command.startswith("type"):

            text = command.replace("type", "").strip()

            type_text(text)

            speak("Typing")

            continue


        # press enter

        if "press enter" in command:

            press_key("enter")

            speak("Done")

            continue


        # open windows search

        if "open search" in command:

            open_search()

            speak("Opening search")

            continue


        # reminders
        if "remind me" in command:
            try:
                words = command.split()
                seconds = int(words[-2])
                message = command.replace("remind me to","").split("in")[0].strip()
                reminder_timer(seconds,message,speak)
                speak("Reminder set")
            except:
                speak("I could not understand the reminder")
            continue

        if "read screen" in command:
            text = read_screen_text()
            speak("I see the following text")
            speak(text)
            continue

        # AI response
        reply = ask_ai(command)
        speak(reply)
        if "click" in command:
            name = command.replace("click","").strip() + ".png"
            if click_image(name):
                speak("Clicked")
            else:
                speak("I could not find that on the screen")
            continue