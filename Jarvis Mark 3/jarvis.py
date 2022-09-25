import imp
from flask import Flask, render_template
import webbrowser as wb
import requests
import speech_recognition as sr
import pyttsx3
import pyaudio
from flask import Flask, render_template

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voices', voices[len(voices) - 1].id)


def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


def SpeakText(command):

    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


app = Flask(__name__)


def index():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 400
        audio = r.listen(source)
    try:
        print("Recognizing")
        query = r.recognize_google(audio, language='en-in')
        r = requests.post('https://api.carterapi.com/v0/chat', json={
            'api_key': '#',  # change it
            'query': query,
            'uuid': "user-id-#",  # change
        })
        agent_response = r.json()
        speak(agent_response=r.json())
    except Exception as e:
        SpeakText(agent_response['output']['text'])
        return render_template("index.html", text=(agent_response['output']['text']))

    
@app.route("/")
while True:
    index()
    
    
app.run(host="0.0.0.0", port=80)
