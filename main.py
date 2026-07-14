import os
import json
import requests
import pandas as pd
import asyncio
from telegram import Bot

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

SYMBOL = "BTCUSDT"
INTERVAL = "5m"

STATE_FILE = "state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"last_signal": "", "last_candle": 0}
    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def get_klines():
    url = (
        f"https://api.binance.com/api/v3/klines"
        f"?symbol={SYMBOL}&interval={INTERVAL}&limit=100"
    )

    data = requests.get(url, timeout=20).json()

    df = pd.DataFrame(
        data,
        columns=[
            "open_time", "open", "high", "low", "close",
            "volume", "close_time", "q", "n", "tbb", "tbq", "ignore"
        ],
    )

    df["close"] = df["close"].astype(float)

    return df


def macd(df):
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()

    macd_line = ema12 - ema26
    signal = macd_line.ewm(span=9, adjust=False).mean()

    return macd_line, signal


async def send(text):
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text)


async def main():

    state = load_state()

    df = get_klines()

    macd_line, signal = macd(df)

    prev_macd = macd_line.iloc[-2]
    curr_macd = macd_line.iloc[-1]

    prev_signal = signal.iloc[-2]
    curr_signal = signal.iloc[-1]

    candle = int(df["close_time"].iloc[-1])

    if candle == state["last_candle"]:
        return

    state["last_candle"] = candle

    if prev_macd < prev_signal and curr_macd > curr_signal:

        if state["last_signal"] != "BUY":
            await send(
                f"🟢 BTCUSDT\n\nBullish MACD Cross\nTimeframe: 5m\nPrice: {df['close'].iloc[-1]}"
            )
            state["last_signal"] = "BUY"

    elif prev_macd > prev_signal and curr_macd < curr_signal:

        if state["last_signal"] != "SELL":
            await send(
                f"🔴 BTCUSDT\n\nBearish MACD Cross\nTimeframe: 5m\nPrice: {df['close'].iloc[-1]}"
            )
            state["last_signal"] = "SELL"

    save_state(state)


asyncio.run(main())
