import logging
import os

from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import CommandHandler, MessageHandler, filters

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await update.message.reply_text('Welcome')


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', send_message))

    app.run_polling()


if __name__ == "__main__":
    main()
