import requests
import pandas as pd
from config import *

URL = "https://api.bybit.com/v5/market/kline"


def get_dataframe():

    response = requests.get(
        URL,
        params={
            "category": "linear",
            "symbol": SYMBOL,
            "interval": INTERVAL.replace("m", ""),
            "limit": LIMIT,
        },
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()["result"]["list"]

    data.reverse()

    df = pd.DataFrame(data)

    df.columns = [
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "turnover",
    ]

    df["close"] = df["close"].astype(float)

    return df


def calculate():

    df = get_dataframe()

    ema12 = df["close"].ewm(span=FAST_EMA, adjust=False).mean()
    ema26 = df["close"].ewm(span=SLOW_EMA, adjust=False).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=SIGNAL_EMA, adjust=False).mean()

    ema200 = df["close"].ewm(span=EMA_FILTER, adjust=False).mean()

    return df, macd, signal, ema200
