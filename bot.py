import openai
import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Fetch API Key securely
openai.api_key = os.getenv("OPENAI_API_KEY")

# Bot Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ Error:\n{str(e)}")

# Main Bot Setup
async def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot is running...")
    await app.run_polling()

# Safe startup for any environment (Render included)
if __name__ == "__main__":
    try:
        asyncio.get_running_loop().create_task(main())
    except RuntimeError:
        asyncio.run(main())
