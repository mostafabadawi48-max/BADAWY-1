import os
import time
import subprocess
import pyttsx3
import ollama
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# تهيئة محرك الصوت
engine = pyttsx3.init()
def speak(text_to_speak, text_to_print):
    print(f"\n[BADAWY-1]: {text_to_print}")
    engine.say(text_to_speak)
    engine.runAndWait()

# دالة استدعاء الذكاء الاصطناعي (مخرجات بالإنجليزية لضمان القراءة السليمة بالـ Terminal)
def ask_ai_about_file(filename, file_content):
    try:
        print(f"\n[🧠] Analyzing content of {filename}...")
        prompt = f"The user updated a file named '{filename}'. Its content is now:\n\"{file_content}\"\nProvide a very brief, smart, and actionable advice or summary based on this content in English (strictly maximum 2 lines)."
        
        response = ollama.generate(model='llama3', prompt=prompt)
        ai_reply = response['response']
        return ai_reply
    except Exception as e:
        return f"Error connecting to AI core: {e}"

# دالة الرفع التلقائي المبسطة
def auto_github_push(filename):
    try:
        subprocess.run("git add .", shell=True)
        subprocess.run(f'git commit -m "Auto-update: {filename}"', shell=True)
        # لو الـ push بيعلق، الكود هيكمل عادي مش هيوقف البرنامج
        subprocess.run("git push", shell=True)
        print(f"[✔] System synced.")
    except:
        print(f"[!] Git operation recorded locally.")

class BadawyFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_triggered = 0

    def on_modified(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            
            # منع التكرار السريع في نفس الثانية (Debounce)
            current_time = time.time()
            if current_time - self.last_triggered < 2:
                return
                
            # مراقبة الملفات النصية فقط وتجاهل ملفات النظام والجيت
            if filename.endswith('.txt') or filename.endswith('.md'):
                if not filename.startswith('~') and '.git' not in event.src_path:
                    self.last_triggered = current_time
                    print(f"\n[!] Change Detected in: {filename}")
                    
                    try:
                        with open(event.src_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except:
                        content = ""
                    
                    # 1. الرفع تلقائياً
                    auto_github_push(filename)
                    
                    # 2. تحليل الـ AI بالإنجليزية نطقاً وكتابة منعاً لأي تهنيج
                    ai_advice = ask_ai_about_file(filename, content)
                    speak(ai_advice, ai_advice)

def start_system():
    print("=========================================")
    print("  BADAWY-1: AUTONOMOUS AI AGENT v2.2    ")
    print("=========================================")
    speak("System Online. AI Agent is ready.", "System Online. AI Agent is ready.")
    
    event_handler = BadawyFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        speak("System Offline.", "System Offline.")
    observer.join()

if __name__ == "__main__":
    start_system()