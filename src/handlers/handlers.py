# from app import logger
from telegram import Update
from telegram.ext import ContextTypes
from ..models.users import (load_user_ids, save_user_ids)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Saves user ID and sends a welcome message."""
    user_id = update.effective_chat.id
    user_ids = load_user_ids()
    if user_id not in user_ids:
        user_ids.add(user_id)
        save_user_ids(user_ids)
        # logger.info(f"New user {user_id} started the bot and was saved.")

    welcome_text = (
        "Hello! I'm your personal weather bot.\n"
        "You're now subscribed to daily forecasts at 7 AM and 11 PM."
    )
    await context.bot.send_message(chat_id=user_id, text=welcome_text)