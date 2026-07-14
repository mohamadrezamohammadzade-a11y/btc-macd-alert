import os
from telegram import Bot

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

bot = Bot(token=BOT_TOKEN)


async def send_message(text):
    await bot.send_message(
        chat_id=CHAT_ID,
        text=text,
    )
