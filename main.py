import asyncio
import json
from datetime import datetime
from zoneinfo import ZoneInfo

from config import SYMBOL, DEBUG
from macd import calculate
from telegram_service import send_message

STATE_FILE = "state.json"


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


async def main():

    df, macd, signal, ema200 = calculate()

    prev_macd = macd.iloc[-3]
    curr_macd = macd.iloc[-2]

    prev_signal = signal.iloc[-3]
    curr_signal = signal.iloc[-2]

    price = float(df["close"].iloc[-2])

    trend_up = price > ema200.iloc[-2]
    trend_down = price < ema200.iloc[-2]

    state = load_state()
    last_signal = state.get("last_signal", "")

    if DEBUG:

        text = f"""📊 BTCUSDT STATUS

💰 Price : {price:.2f}

MACD : {curr_macd:.4f}
Signal : {curr_signal:.4f}

EMA200 : {ema200.iloc[-2]:.2f}

Trend :
{"🟢 Bullish" if trend_up else "🔴 Bearish"}

MACD Position :
{"🟢 Above Signal" if curr_macd > curr_signal else "🔴 Below Signal"}
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

        if last_signal != "BUY":

            await send_message(
                f"""🟢 BUY SIGNAL

🪙 {SYMBOL}

💰 Price : {price:.2f}

📈 MACD Bullish Cross

🕒 {tehran_time}
"""
            )

            save_state({"last_signal": "BUY"})

    elif (
        prev_macd > prev_signal
        and curr_macd < curr_signal
        and trend_down
    ):

        if last_signal != "SELL":

            await send_message(
                f"""🔴 SELL SIGNAL

🪙 {SYMBOL}

💰 Price : {price:.2f}

📉 MACD Bearish Cross

🕒 {tehran_time}
"""
            )

            save_state({"last_signal": "SELL"})


if __name__ == "__main__":
    asyncio.run(main())
