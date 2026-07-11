import os
import sys
from datetime import datetime
import arabic_reshaper
from bidi.algorithm import get_display

# إعدادات الترميز الأساسية للتيرمنال
if sys.platform.startswith('win'):
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')

def fix_text(text):
    """إصلاح النص العربي المقلوب والمقطع ليظهر سليماً في التيرمنال"""
    if not text.strip():
        return text
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def write_to_file(file_path, text):
    """دالة مساعدة للكتابة في الملفات مع إضافة التوقيت"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry = f"* [{current_time}] {text}\n"
    
    with open(file_path, "a", encoding="utf-8") as file:
        file.write(log_entry)

def interactive_logger():
    """نظام التوثيق التفاعلي الذكي لمنع النسيان"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50)
    print(fix_text("📝 نظام BADAWY-1 للتوثيق الذكي المطور"))
    print("="*50)
    
    print(fix_text("اختر نوع التوثيق الذي تريد تسجيله الآن:"))
    print(fix_text("1 - إنجاز أو تحديث في العمل/المشروع (AI_LOG.md)"))
    print(fix_text("2 - تحديث في الحالة الشخصية أو الأهداف (CURRENT_STATUS.md)"))
    print(fix_text("3 - العودة لـ لوحة التحكم (Dashboard)"))
    print("="*50)
    
    # تركنا الـ input هنا بدون fix_text لكي يقرأ الرقم الإنجليزي/العادي بشكل سليم ومباشر
    choice = input(">>> ").strip()
    
    if choice == "1":
        print(fix_text("اكتب الإنجاز الذي قمت به اليوم ثم اضغط Enter:"))
        note = input(">>> ")
        if note.strip():
            write_to_file("AI_LOG.md", note)
            print(fix_text(f"✅ تم تسجيل الإنجاز بنجاح في AI_LOG.md"))
        else:
            print(fix_text("⚠️ لم يتم كتابة أي شيء."))
            
    elif choice == "2":
        print(fix_text("اكتب التحديث الجديد لحالتك أو أهدافك ثم اضغط Enter:"))
        note = input(">>> ")
        if note.strip():
            write_to_file("CURRENT_STATUS.md", note)
            print(fix_text(f"✅ تم تحديث الحالة بنجاح في CURRENT_STATUS.md"))
        else:
            print(fix_text("⚠️ لم يتم كتابة أي شيء."))
            
    elif choice == "3":
        display_dashboard()
    else:
        # طباعة ما تم إدخاله لنعرف المشكلة إذا تكررت
        print(fix_text(f"❌ اختيار غير صحيح. أنت قمت بإدخال: {choice}"))

def display_dashboard():
    """عرض لوحة التحكم اليومية"""
    dashboard_path = os.path.join("DASHBOARD", "HOME.md")
    
    if not os.path.exists(dashboard_path):
        print(fix_text(f"❌ لم يتم العثور على الـ Dashboard في المسار: {dashboard_path}"))
        return
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50)
    print("🤖 BADAWY-1 | DAILY DASHBOARD")
    print("="*50)
    
    try:
        with open(dashboard_path, "r", encoding="utf-8") as file:
            content = file.read()
            print(fix_text(content))
    except Exception as e:
        print(fix_text(f"❌ حدث خطأ أثناء قراءة الملف: {e}"))
        
    print("="*50 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--log":
        interactive_logger()
    else:
        display_dashboard()