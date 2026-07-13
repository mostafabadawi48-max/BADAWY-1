import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from badawy_core import ask_groq
from memory import save_conversation

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 جارفيس جاهز! ابعتلي أي رسالة وهرد عليك.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = ask_groq(user_input)
    save_conversation(user_input, response)
    await update.message.reply_text(response)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 البوت شغال دلوقتي على تليجرام...")
    app.run_polling()

if __name__ == "__main__":
    main()