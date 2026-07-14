from telegram import Bot
from config import *
import asyncio

bot = Bot(token=TELEGRAM_BOT_TOKEN)


async def send_message(text):

    await bot.send_message(
        chat_id=TELEGRAM_CHAT_ID,
        text=text
    )
