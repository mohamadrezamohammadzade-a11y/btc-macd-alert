import asyncio
from datetime import datetime
from zoneinfo import ZoneInfo

from config import SYMBOL, DEBUG
from macd import calculate
from telegram_service import send_message


async def main():
    raise Exceptoin("TEST 123")
    df, macd, signal, ema200 = calculate()

    # فقط کندل‌های بسته شده
    prev_macd = macd.iloc[-3]
    curr_macd = macd.iloc[-2]

    prev_signal = signal.iloc[-3]
    curr_signal = signal.iloc[-2]

    price = float(df["close"].iloc[-2])

    trend_up = price > ema200.iloc[-2]
    trend_down = price < ema200.iloc[-2]

    if DEBUG:

        text = f"""📊 BTCUSDT STATUS

💰 Price: {price:.2f}

MACD : {curr_macd:.4f}
Signal : {curr_signal:.4f}

EMA200 : {ema200.iloc[-2]:.2f}

Trend :
{"🟢 Bullish" if trend_up else "🔴 Bearish"}

MACD Position :
{"🟢 Above Signal" if curr_macd > curr_signal else "🔴 Below Signal"}

Bullish Cross :
{"✅ YES" if prev_macd < prev_signal and curr_macd > curr_signal else "❌ NO"}

Bearish Cross :
{"✅ YES" if prev_macd > prev_signal and curr_macd < curr_signal else "❌ NO"}
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

        await send_message(
            f"""🟢 BUY SIGNAL

🪙 {SYMBOL}

💰 Price : {price:.2f}

📈 MACD Bullish Cross

🕒 {tehran_time}
"""
        )

    elif (
        prev_macd > prev_signal
        and curr_macd < curr_signal
        and trend_down
    ):

        await send_message(
            f"""🔴 SELL SIGNAL

🪙 {SYMBOL}

💰 Price : {price:.2f}

📉 MACD Bearish Cross

🕒 {tehran_time}
"""
        )


if name == "__main__":
    asyncio.run(main())
