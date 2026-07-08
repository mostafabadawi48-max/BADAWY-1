import os
import time
import subprocess
import pyttsx3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# تهيئة محرك الصوت
engine = pyttsx3.init()
def speak(text):
    print(f"[BADAWY-1 Voice]: {text}")
    engine.say(text)
    engine.runAndWait()

# دالة الرفع التلقائي على GitHub
def auto_github_push(filename):
    try:
        print(f"\n[🔄] Starting Auto-Sync to GitHub for: {filename}...")
        # تنفيذ أوامر الجيت تلقائياً
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Auto-update: {filename} via BADAWY-1 Core"], check=True)
        subprocess.run(["git", "push"], check=True)
        
        speak(f"File {filename} successfully synced to GitHub.")
    except Exception as e:
        print(f"[X] GitHub Sync Error: {e}")
        speak("GitHub sync encountered an error.")

class BadawyFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            # تجنب الملفات المؤقتة وملفات الجيت والنظام
            if not filename.endswith('.tmp') and not filename.startswith('~') and '.git' not in event.src_path:
                print(f"\n[!] Change Detected in: {filename}")
                # تشغيل الرفع التلقائي فوراً
                auto_github_push(filename)

def start_system():
    print("=========================================")
    print("   BADAWY-1: AUTONOMOUS CORE ACTIVE v1.2 ")
    print("=========================================")
    speak("Autonomous core is online and tracking your files.")
    
    event_handler = BadawyFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        speak("System going offline.")
    observer.join()

if __name__ == "__main__":
    start_system()