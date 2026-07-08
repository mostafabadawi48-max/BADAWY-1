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
    print(f"[BADAWY-1]: {text_to_print}")
    engine.say(text_to_speak)
    engine.runAndWait()

# دالة استدعاء الذكاء الاصطناعي
def ask_ai_about_file(filename, file_content):
    try:
        print(f"\n[🧠] BADAWY-1 Brain is analyzing {filename}...")
        prompt = f"المستخدم قام بتحديث ملف اسمه {filename}. المحتوى الحالي:\n\"{file_content}\"\nبناءً على هذا، أعطني نصيحة أو تعليق ذكي وموجز جداً بالعامية المصرية (في سطر واحد فقط)."
        
        response = ollama.generate(model='llama3', prompt=prompt)
        ai_reply = response['response']
        
        # حفظ الرد العربي في ملف نظيف حتى لا يظهر معكوساً في الـ Terminal
        with open("AI_LOG.txt", "w", encoding="utf-8") as log_file:
            log_file.write(f"=== BADAWY-1 Advice for {filename} ===\n{ai_reply}\n")
            
        return ai_reply
    except Exception as e:
        print(f"[X] AI Error: {e}")
        return "تم التحديث"

# دالة الرفع المحسنة على GitHub
def auto_github_push(filename):
    try:
        # استخدام shell=True لتفادي مشاكل الويندوز في الـ Git
        subprocess.run("git add .", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(f'git commit -m "Auto-update: {filename}"', shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run("git push origin main", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[✔] GitHub synced successfully.")
    except Exception as e:
        print(f"[!] GitHub auto-commit created locally (Push skipped or needs configuration).")

class BadawyFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            # تجنب ملفات الـ Log والملفات المؤقتة لمنع اللوب اللانهائي
            if not filename.endswith('.tmp') and not filename.startswith('~') and filename != "AI_LOG.txt" and '.git' not in event.src_path:
                print(f"\n[!] Change Detected in: {filename}")
                
                try:
                    with open(event.src_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                except:
                    content = ""
                
                auto_github_push(filename)
                ai_advice = ask_ai_about_file(filename, content)
                
                # ينطق العربي، ولكن يطبع رسالة إنجليزية بالـ Terminal منعا للحروف المعكوسة
                speak(ai_advice, f"Analysis done! Check 'AI_LOG.txt' to read my advice.")

def start_system():
    print("=========================================")
    print("  BADAWY-1: AUTONOMOUS AI AGENT v2.1    ")
    print("=========================================")
    speak("System Online.", "System Online. AI Agent is ready.")
    
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