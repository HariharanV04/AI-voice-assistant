import streamlit as st
import speech_recognition as sr
import pyttsx3 as tts
recognizer = sr.Recognizer()
tts = tts.init()

from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

client = OpenAI()

import requests
import os
import datetime
import time
from playsound import playsound
import threading
from datetime import *

now = datetime.now()
nows = now.strftime("%H:%M")

WEATHER_API = os.getenv("WEATHER_API")
city="Chennai"
weather_url = f"http://api.openweathermap.org/data/2.5/weather?appid={WEATHER_API}&q={city}&units=metric"

st.set_page_config(
page_title="Dashboard",
layout="wide",
)

st.title("Welcome to Victopia")
st.header("Voice assistant")
st.markdown("Say hello to Victoria")

weather_response = requests.get(weather_url).json()
weat = weather_response["weather"][0]['main']
des = weather_response["weather"][0]['description']

w1, w2, w3, w4 = st.columns(4)
w1.metric(
label="Weather",
value=f"{weat}" ,
)

w2.metric(
label="Temperature ",
value=f"{int(weather_response["main"]["temp"])}°C",
delta= weather_response["main"]["temp_max"]- weather_response["main"]["temp_min"],
)

w3.metric(
label="What it feels like ",
value=f"{int(weather_response["main"]["feels_like"])}°C",

)

w4.metric(
label="Time ",
value=f"{nows}",

)

def play_alarm_sound():
    playsound("prowler_theme.mp3")

def check_alarm(alarm_time):
    while True:
        current_time = datetime.now().strftime("%H:%M")
        if current_time == (alarm_time):
            st.session_state["alarm_triggered"] = True
            threading.Thread(target=play_alarm_sound).start()
            break

alarm_word = "alarm set at"
wake_word = "hello victoria"
sleep_word = "stop talking"
def talker(topic):
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
    {"role": "system", "content": """You are a friendly voice assistant, named Victoria. When an user asks you to set
    an alarm(e.g set an alarm for 7 AM), you should
    display a confirmation of their request with a reply containing the timing in 24 hour format
    (e.g. Alarm set at 07:00).
    But you do not have the ability to set the alarm itself. If the command is unclear, ask again."""},
    {"role": "user", "content": topic},
    ],
    temperature=0.8,   # More creative!
    max_tokens=500,    # Longer story
    top_p=1,
    frequency_penalty=0.3,  # Less repetitive
    presence_penalty=0.6    # Encourages talking about new topics
    )
    return response.choices[0].message.content

with sr.Microphone() as mic:
    st.write("Hi...  (^-^)  ")
    unrecognized_voice = False

    
    while True:
        try:
            recognizer.adjust_for_ambient_noise(mic, duration=1)
            audio = recognizer.listen(mic)
            text = recognizer.recognize_google(audio).lower()
            #print(f"You said: {text}")
            unrecognized_voice = False

            if wake_word in text:
                st.write("Hi, how may I be of service...")

                while True:
                    try:
                        recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                        audio = recognizer.listen(mic)
                        spoken = recognizer.recognize_google(audio).lower()

                        if sleep_word in spoken:
                            st.write("(>_<)...")
                            break
                            #st.write(replied[-6:-1])
                            
                        else:
                            st.write("User query:", spoken)
                            replied = talker(spoken)  
                            if alarm_word in replied.lower():
                                alarmt = replied[-6:-1]
                                alarm_time = datetime.strptime(alarmt,'%H:%M')
                                st.success(f"Alarm set for {alarmt}")
                                check_alarm(alarmt)
                                st.session_state["alarm_triggered"] = False
                                threading.Thread(target=check_alarm, args=(alarm_time,), daemon=True).start()
                                if st.session_state.get("alarm_triggered"):
                                    st.warning("🚨 Alarm is ringing!")
                                continue
                            st.write(replied)
                    
                            

                    except sr.UnknownValueError:
                        if not unrecognized_voice:
                            st.write("Pardon... (o_O)")
                            unrecognized_voice = True
                        recognizer = sr.Recognizer()

        except sr.UnknownValueError:
            if not unrecognized_voice:
                st.write("Pardon... (o_O)")
                unrecognized_voice = True
            recognizer = sr.Recognizer()


#print(response)
#print(response.choices\[0].message.content)
