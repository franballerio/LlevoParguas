import logging
import os
import openmeteo_requests
import pandas as pd
import requests_cache

from weather_api import fetch_weather, parse_weather
from retry_requests import retry
from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import CommandHandler, MessageHandler, filters

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Configure logging (good practice to have it in your main entry point)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
	weather_df = fetch_weather()
	msg = parse_weather(weather_df)
    
	return update.message.reply_text(msg)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', send_message))

    app.run_polling()


if __name__ == "__main__":
    main()
