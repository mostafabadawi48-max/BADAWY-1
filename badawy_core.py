import os
import time
import subprocess
import pyttsx3
import ollama
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# تهيئة محرك الصوت
engine = pyttsx3.init()
def speak(text):
    print(f"[BADAWY-1 Voice]: {text}")
    engine.say(text)
    engine.runAndWait()

# دالة استدعاء الذكاء الاصطناعي المحلي (Llama 3)
def ask_ai_about_file(filename, file_content):
    try:
        print(f"\n[🧠] BADAWY-1 Brain is analyzing content of {filename}...")
        prompt = f"المستخدم قام بتحديث ملف اسمه {filename}. محتوى الملف الحالي هو:\n\"{file_content}\"\nبناءً على هذا التحديث، أعطني تعليقاً أو نصيحة أو ملخصاً ذكياً وموجزاً جداً بالعامية المصرية (في سطرين فقط) لأسجله صوتياً للمستخدم."
        
        response = ollama.generate(model='llama3', prompt=prompt)
        ai_reply = response['response']
        return ai_reply
    except Exception as e:
        print(f"[X] AI Error: {e}")
        return "تم تحديث الملف بنجاح، لكن واجهت مشكلة في الاتصال بالعقل المحلي."

# دالة الرفع التلقائي على GitHub
def auto_github_push(filename):
    try:
        print(f"[🔄] Syncing to GitHub...")
        subprocess.run(["git", "add", "."], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "commit", "-m", f"Auto-update: {filename}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "push"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[✔] GitHub synced.")
    except Exception as e:
        print(f"[X] GitHub Sync Error: {e}")

class BadawyFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            if not filename.endswith('.tmp') and not filename.startswith('~') and '.git' not in event.src_path:
                print(f"\n[!] Change Detected in: {filename}")
                
                # قراءة محتوى الملف لمعالجته بالذكاء الاصطناعي
                try:
                    with open(event.src_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except:
                    content = ""
                
                # 1. الرفع على جيت هاب تلقائياً
                auto_github_push(filename)
                
                # 2. سؤال الذكاء الاصطناعي عن التعديل
                ai_advice = ask_ai_about_file(filename, content)
                
                # 3. نطق النصيحة الذكية
                speak(ai_advice)

def start_system():
    print("=========================================")
    print("  BADAWY-1: AUTONOMOUS AI AGENT v2.0    ")
    print("=========================================")
    speak("System Online. AI Agent is ready.")
    
    event_handler = BadawyFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        speak("System Offline.")
    observer.join()

if __name__ == "__main__":
    start_system()