import os
import sys
import requests
import json
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display

try:
    import pyttsx3
    engine = pyttsx3.init()
except ImportError:
    engine = None

if sys.platform.startswith('win'):
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

OLLAMA_MODEL = "llama3" 
OLLAMA_URL = "http://localhost:11434/api/generate"

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

def ask_ollama(prompt):
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    try:
        # تم زيادة الـ timeout إلى 60 ثانية
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        if response.status_code == 200:
            return response.json().get("response", "")
        return f"Error code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"

def ai_agent_chat():
    os.system('cls' if os.name == 'nt' else 'clear')
    welcome = "🤖 جارفيس الشخصي جاهز ومستمع إليك الآن. اكتب 'خروج' للإنهاء."
    print("="*50)
    print(fix_text(welcome))
    print("="*50)
    speak_text("جارفيس جاهز ومستمع إليك الآن")

    dashboard_context = ""
    dashboard_path = os.path.join("DASHBOARD", "HOME.md")
    if os.path.exists(dashboard_path):
        with open(dashboard_path, "r", encoding="utf-8") as f:
            dashboard_context = f.read()

    while True:
        # الإدخال عادي، التيرمنال سيعرضه مشوهاً أثناء الكتابة لكن الكود سيصلحه بالخلفية
        user_input = input("You >>> ")
        if user_input.strip().lower() in ["خروج", "exit", "quit"]:
            break
            
        if not user_input.strip():
            continue

        # إصلاح النص برمجياً قبل إرساله للموديل ليقرأه صحيحاً
        fixed_user_input = get_display(arabic_reshaper.reshape(user_input))

        full_prompt = f"""
        You are BADAWY-1 (Jarvis), a smart AI Personal Assistant. 
        Respond in short, clear, and helpful Arabic so it can be spoken easily.
        Context: {dashboard_context}
        User: {fixed_user_input}
        Assistant:"""
        
        print(fix_text("⏳ جارفيس يفكر ويتحدث..."))
        ai_response = ask_ollama(full_prompt)
        
        print("\n" + "="*50)
        print(fix_text(ai_response))
        print("="*50 + "\n")
        
        speak_text(ai_response)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--agent":
        ai_agent_chat()