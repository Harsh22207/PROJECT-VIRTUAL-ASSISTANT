import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from gtts import gTTS
import pygame
import os
import API_KEY

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = API_KEY.key["NEWS_API_KEY"]

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    #initialize pygame
    pygame.mixer.init()

    #load the mp3 file
    pygame.mixer.music.load('temp.mp3')

    #play mp3 file
    pygame.mixer.music.play()

    #keeps program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")    


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com/")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")
        song.pop(0)
        song = " ".join(song)
        webbrowser.open(musicLibrary.music[song])


# make jarvis tell news headlines using news api

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            #pasrse the JSON response
            data = r.json()

            #extract the articles
            articles = data.get('articles', [])

            #print the headlines
            for article in articles:
                speak(article['title'])

    # let OpenAI handle the request 

    else:
        pass
    
        
if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
    #listen for wake word "jarvis"
    # obtain audio from the microphone
        r = sr.Recognizer()
        
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening")
                audio = r.listen(source, timeout=3, phrase_time_limit=2)
            Wake_word = r.recognize_google(audio)
            if(Wake_word.lower() == "jarvis"):
                speak("How can I help you today?")
                #listen for command
                with sr.Microphone() as source:
                    print("Jarvis is listening...")
                    audio = r.listen(source, timeout=4, phrase_time_limit=3)
                command = r.recognize_google(audio)

                processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))

