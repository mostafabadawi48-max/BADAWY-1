import os
import sys
from memory import save_conversation, get_recent_memory
from groq import Groq
import json
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
def load_brain_context():
    brain_folder = "Brain"
    context_parts = []
    if os.path.exists(brain_folder):
        for filename in os.listdir(brain_folder):
            if filename.endswith(".md"):
                filepath = os.path.join(brain_folder, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    context_parts.append(f"--- {filename} ---\n{content}")
    dashboard_path = os.path.join("DASHBOARD", "HOME.md")
    if os.path.exists(dashboard_path):
        with open(dashboard_path, "r", encoding="utf-8") as f:
            context_parts.append(f"--- HOME.md ---\n{f.read()}")
        return "\n\n".join(context_parts)
def listen_from_mic(duration=5, samplerate=44100):
    print(fix_text("🎤 اتكلم دلوقتي..."))
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    wav.write("temp_audio.wav", samplerate, recording)

    recognizer = sr.Recognizer()
    with sr.AudioFile("temp_audio.wav") as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language="ar-EG")
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return f"Error: {e}"
try:
    import pyttsx3
    engine = pyttsx3.init()
except ImportError:
    engine = None

if sys.platform.startswith('win'):
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

GROQ_MODEL = "llama-3.3-70b-versatile"
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def fix_text(text):
    if not text.strip():
        return text
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def speak_text(text):
    if engine:
        clean_text = text.replace("🤖", "").replace("✅", "").replace("⏳", "")
        engine.say(clean_text)
        engine.runAndWait()

def ask_groq(prompt):
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def ai_agent_chat():
    os.system('cls' if os.name == 'nt' else 'clear')
    welcome = "🤖 جارفيس الشخصي جاهز ومستمع إليك الآن. اكتب 'خروج' للإنهاء."
    print("="*50)
    print(fix_text(welcome))
    print("="*50)
    speak_text("جارفيس جاهز ومستمع إليك الآن")

    memory_context = get_recent_memory(5)
    brain_context = load_brain_context()
    while True:
        print(fix_text("اكتب 'صوت' عشان تتكلم، أو اكتب رسالتك عادي:"))
        typed = input("You >>> ")
        if typed.strip() == "صوت":
            user_input = listen_from_mic()
            print(fix_text(f"سمعتك بتقول: {user_input}"))
        else:
            user_input = typed

        if user_input.strip().lower() in ["خروج", "exit", "quit"]:
            break

        if not user_input.strip():
            continue
        response = ask_groq(user_input)
        print(fix_text(f"🤖 {response}"))
        speak_text(response)
        save_conversation(user_input, response)

if __name__ == "__main__":
    if "--agent" in sys.argv:
        ai_agent_chat()
    else:
        print("استخدم --agent لتشغيل البرنامج")