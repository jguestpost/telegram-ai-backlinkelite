import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import openai

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_GROUP_ID = int(os.getenv("TARGET_GROUP_ID"))
TANYA_AI_THREAD_ID = int(os.getenv("TANYA_AI_THREAD_ID"))

openai.api_key = OPENAI_API_KEY

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    # Cetak ID Grup & Thread
    print("Chat ID:", message.chat.id)
    print("Thread ID:", message.message_thread_id)
    print("User Text:", message.text)

    await message.reply_text("📡 Bot aktif. Cek log di Render untuk ID-nya.")


if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()
