#!/usr/bin/env python
# coding: utf-8

import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import sys
import webbrowser
from datetime import date
import os
import time
import re

engine = pyttsx3.init()
voices = engine.getProperty("voices")

engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 200)

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"

def WishMyMaster():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        print("Good morning sir!")
        engine_talk("good morning sir")
    elif hour>=12 and hour <16:
        print("Good afternoon sir!")
        engine_talk("good afternoon sir")
    else:
        print("Good evening sir!")
        engine_talk("Good evening sir")
    print("I am SideKick")
    engine_talk("I am Sidekick")

def engine_talk(text):
    engine.say(text)
    engine.runAndWait()
    
def engine_listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        r.dynamic_energy_threshold = True
        r.pause_threshold = 1
        r.operation_timeout = 1
        print('\n')
        print("Listening...")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language = "en-US").lower()
        return query
    except:
        engine_talk("Please repeat that one")
        engine_listen()
    
def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

def yesno(query):
    if "yes" or "ya" or "yeah" in query:
        return "yes"
    elif "no" or "nah" in query:
        return "no"
    else:
        engine_talk("Please repeat")
        engine_listen()
        yesno()

def SideKick():
    print("How may I help you?")
    engine_talk("How may i help you?")
    query = engine_listen()
    print(query)
    
    if 'wikipedia' in query:
        engine_talk("searching...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences = 10)
        sentences = split_into_sentences(results)
        engine_talk("According to wikipedia, " + sentences[0])
        
    elif 'how are you' or 'how you doing' in query:
        print('I am good, what about you?')
        engine_talk('I am good, what about you?')
        query = engine_listen()
        if 'bad' in query:
            print("Everything will be alright, sir")
            engine_talk("Everything will be alright, sir")
        elif 'good' or 'better' in query:
            print("Good to hear, sir.")
            engine_talk("Good to hear, sir.")

    elif 'open' in query:
        if 'youtube' in query:
            webbrowser.open("youtube.com")
        elif 'google' in query:
            webbrowser.open("google.com")
        elif 'chrome' or 'browser' in query:
            webpath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
            os.startfile(webpath)
   
    elif 'bye' in query:
        print('good bye, have a nice day !!')
        engine_talk('good bye, have a nice day !!')
        sys.exit()

    elif 'play' in query:
        if 'music' in query:
            music_dir = "C:\\Users\\thepr\\Music\\SONGS"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

    elif 'time' or 'date' in query:
        if 'date' in query and 'time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            today = date.today()
            strdate = today.strftime("%D")
            print("Time is", strtime)
            print("Date is", strdate)
            engine_talk(f"Sir, the time is {strtime} and today is {strdate}")
        elif 'time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strtime)
            engine_talk(f"Sir, the time is {strtime}")
        elif 'date' in query:
            today = date.today()
            strdate = today.strftime("%D")
            print(strdate)
            engine_talk(f"Sir, the date is {strdate}")
       

WishMyMaster()
SideKick()
