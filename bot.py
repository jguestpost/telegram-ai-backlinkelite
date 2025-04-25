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

    # Pastikan ini dari grup dan topik yang tepat
    if message and message.chat.id == TARGET_GROUP_ID and message.message_thread_id == TANYA_AI_THREAD_ID:
        try:
            user_text = message.text

            response = openai.ChatCompletion.create(
                model="GPT -4o",
                messages=[{"role": "user", "content": user_text}]
            )

            reply = response['choices'][0]['message']['content']
            await message.reply_text(reply, message_thread_id=TANYA_AI_THREAD_ID)

        except Exception as e:
            await message.reply_text("Maaf, terjadi kesalahan saat menjawab.")
            print("Error:", e)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()
