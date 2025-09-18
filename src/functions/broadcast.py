import asyncio
from ..models.users import (load_user_ids, save_user_ids)
from ..models.weather_api import (fetch_weather, parse_weather)
from telegram.error import Forbidden
from telegram.ext import ContextTypes
from telegram import Update


async def broadcast_job(update: Update, forecast_type: str):
    """A generic function to fetch weather and broadcast it to all users."""
    #logger.info(f"Running broadcast job for: {forecast_type}")
    
    try:
        if forecast_type == 'today':
            weather_df = fetch_weather(today=True)
        else: # tomorrow
            weather_df = fetch_weather()
        
        msg = parse_weather(weather_df)
        
        user_ids = load_user_ids()
        if not user_ids:
            #logger.info("No users to send messages to.")
            return

        failed_ids = set()
        for user_id in user_ids:
            try:
                await update.bot.send_message(chat_id=user_id, text=msg)
                # A small delay to avoid hitting rate limits with many users
                await asyncio.sleep(0.1) 
            except Forbidden:
                #logger.warning(f"User {user_id} blocked the bot. Removing from list.")
                failed_ids.add(user_id)
            #except Exception as e:
                #logger.error(f"Failed to send message to {user_id}: {e}")

        # Remove users who have blocked the bot
        if failed_ids:
            updated_user_ids = user_ids - failed_ids
            save_user_ids(updated_user_ids)

    except Exception as e:
        return
        #logger.error(f"Error in broadcast_job for {forecast_type}: {e}")

async def send_todays_forecast_job(context: ContextTypes.DEFAULT_TYPE):
    """Callback for the 7 AM job."""
    await broadcast_job(context, 'today')

async def send_tomorrows_forecast_job(context: ContextTypes.DEFAULT_TYPE):
    """Callback for the 11 PM job."""
    await broadcast_job(context, 'tomorrow')