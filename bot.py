import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction
import openai

# Load .env
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_GROUP_ID = int(os.getenv("TARGET_GROUP_ID"))
TANYA_AI_THREAD_ID = int(os.getenv("TANYA_AI_THREAD_ID"))

openai.api_key = OPENAI_API_KEY

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    chat_id = message.chat.id
    thread_id = message.message_thread_id
    user_text = message.text

    if chat_id == TARGET_GROUP_ID and thread_id == TANYA_AI_THREAD_ID:
        try:
            # ⏳ Efek mengetik
            await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

            # 🔁 Kirim ke GPT
            response = openai.ChatCompletion.create(
                model="gpt-4o",  # Pastikan ini lowercase & tanpa spasi
                messages=[{"role": "user", "content": user_text}]
            )

            reply = response['choices'][0]['message']['content']
            await message.reply_text(reply, message_thread_id=thread_id)

        except Exception as e:
            print("❌ Error:", e)
            await message.reply_text("⚠️ Maaf, terjadi kesalahan saat menjawab.", message_thread_id=thread_id)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🤖 Bot GPT is running...")
    app.run_polling()
