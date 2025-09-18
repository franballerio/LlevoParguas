import logging
import os

from datetime import time
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from telegram.ext import (ApplicationBuilder, CommandHandler)
from src.functions.broadcast import (send_todays_forecast_job, send_tomorrows_forecast_job)
from src.handlers.handlers import start

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():

    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in .env file. Please set it.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    job_queue = app.job_queue
    buenos_aires_tz = ZoneInfo("America/Argentina/Buenos_Aires")

    job_queue.run_daily(
        send_todays_forecast_job,
        time=time(hour=7, minute=0, tzinfo=buenos_aires_tz),
        name="daily_7am_forecast"
    )

    job_queue.run_daily(
        send_tomorrows_forecast_job,
        time=time(hour=20, minute=42, tzinfo=buenos_aires_tz),
        name="daily_11pm_forecast"
    )

    app.add_handler(CommandHandler("start", start))

    logger.info("Bot started and jobs scheduled for broadcasting.")
    app.run_polling()

if __name__ == "__main__":
    main()

