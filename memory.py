import sqlite3
from datetime import datetime

conn = sqlite3.connect("badawy_memory.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    user_message TEXT,
    ai_response TEXT
)
""")
conn.commit()
def save_conversation(user_message, ai_response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO conversations (timestamp, user_message, ai_response) VALUES (?, ?, ?)",
        (timestamp, user_message, ai_response)
    )
    conn.commit()  
def get_recent_memory(limit=5):
    cursor.execute(
        "SELECT user_message, ai_response FROM conversations ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()
    return rows
cursor.execute("SELECT * FROM conversations")
print(cursor.fetchall())