import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from macd import calculate
from telegram_service import send_message
from config import SYMBOL


async def main():
    df, macd, signal = calculate()

    prev_macd = macd.iloc[-2]
    curr_macd = macd.iloc[-1]

    prev_signal = signal.iloc[-2]
    curr_signal = signal.iloc[-1]

    price = float(df["close"].iloc[-1])

    tehran_time = datetime.now(
        ZoneInfo("Asia/Tehran")
    ).strftime("%Y-%m-%d %H:%M:%S")

    if prev_macd < prev_signal and curr_macd > curr_signal:

        text = f"""🟢 BUY SIGNAL

🪙 {SYMBOL}

💰 Price : {price:.2f}

📈 MACD Bullish Cross

🕒 {tehran_time}
"""

        await send_message(text)

    elif prev_macd > prev_signal and curr_macd < curr_signal:

        text = f"""🔴 SELL SIGNAL

🪙 {SYMBOL}

💰 Price : {price:.2f}

📉 MACD Bearish Cross

🕒 {tehran_time}
"""

        await send_message(text)


if name == "__main__":
    asyncio.run(main())
