import os
import sys
from memory import save_conversation, get_recent_memory
from groq import Groq
import json
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display
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
        user_input = input("You >>> ")
        if user_input.strip().lower() in ["خروج", "exit", "quit"]:
            break

        if not user_input.strip():
            continue

        fixed_user_input = get_display(arabic_reshaper.reshape(user_input))

        full_prompt = f"""
        You are BADAWY-1 (Jarvis), a smart AI Personal Assistant. 
        Respond in short, clear, and helpful Arabic so it can be spoken easily.
        Context: {brain_context}
        Recent memory: {memory_context}
        User: {fixed_user_input}
        Assistant:"""

        print(fix_text("⏳ جارفيس يفكر ويتحدث..."))
        ai_response = ask_groq(full_prompt)

        print("\n" + "="*50)
        print(fix_text(ai_response))
        print("="*50 + "\n")

        speak_text(ai_response)
        save_conversation(fixed_user_input, ai_response)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--agent":
        ai_agent_chat()