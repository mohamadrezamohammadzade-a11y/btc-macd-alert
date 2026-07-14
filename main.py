import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from macd import calculate
from telegram_service import send_message
from config import SYMBOL, DEBUG


async def main():

    df, macd, signal, ema200 = calculate()

    prev_macd = macd.iloc[-2]
    curr_macd = macd.iloc[-1]

    prev_signal = signal.iloc[-2]
    curr_signal = signal.iloc[-1]

    price = float(df["close"].iloc[-1])

    trend_up = price > ema200.iloc[-1]
    trend_down = price < ema200.iloc[-1]

    if DEBUG:

        text = f"""
📊 BTCUSDT STATUS

💰 Price: {price:.2f}

MACD : {curr_macd:.4f}
Signal : {curr_signal:.4f}

EMA200 : {ema200.iloc[-1]:.2f}

Trend :
{"🟢 Bullish" if trend_up else "🔴 Bearish"}

MACD Position :
{"🟢 Above Signal" if curr_macd > curr_signal else "🔴 Below Signal"}

Previous Candle

MACD : {prev_macd:.4f}
Signal : {prev_signal:.4f}
"""

        await send_message(text)
        return

    tehran_time = datetime.now(
        ZoneInfo("Asia/Tehran")
    ).strftime("%Y-%m-%d %H:%M:%S")

    if (
        prev_macd < prev_signal
        and curr_macd > curr_signal
        and trend_up
    ):

        text = f"""🟢 BUY SIGNAL

🪙 {SYMBOL}

💰 Price : {price:.2f}

📈 MACD Bullish Cross

🕒 {tehran_time}
"""

        await send_message(text)

    elif (
        prev_macd > prev_signal
        and curr_macd < curr_signal
        and trend_down
    ):

        text = f"""🔴 SELL SIGNAL

🪙 {SYMBOL}

💰 Price : {price:.2f}

📉 MACD Bearish Cross

🕒 {tehran_time}
"""

        await send_message(text)


if name == "__main__":
    asyncio.run(main())
