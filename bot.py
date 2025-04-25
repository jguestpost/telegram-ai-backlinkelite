import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Konfigurasi Token dan API Key
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Fungsi awal /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot aktif. Kirim pesan ke thread Tanya AI.")

# ✅ Fungsi untuk ambil group ID dan thread ID
async def get_thread_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    thread_id = update.message.message_thread_id
    await update.message.reply_text(f"Group ID: {chat_id}\nThread ID: {thread_id}")


# Jalankan bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Tambahkan handler untuk perintah /start
    app.add_handler(CommandHandler("start", start))

    # Tambahkan ini untuk ambil info thread
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, get_thread_info))

    print("Bot aktif... Kirim pesan ke thread Tanya AI untuk lihat ID-nya.")
    app.run_polling()
