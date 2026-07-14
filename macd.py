import requests
import pandas as pd
from config import *

URL = "https://api.binance.com/api/v3/klines"


def get_dataframe():

    data = requests.get(
        URL,
        params={
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "limit": LIMIT
        },
        timeout=20
    ).json()

    df = pd.DataFrame(data)

    df.columns = [
        "open_time","open","high","low","close",
        "volume","close_time",
        "q","n","tbb","tbq","ignore"
    ]

    df["close"] = df["close"].astype(float)

    return df


def calculate():

    df = get_dataframe()

    ema12 = df.close.ewm(span=FAST_EMA).mean()
    ema26 = df.close.ewm(span=SLOW_EMA).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=SIGNAL_EMA).mean()

    return df, macd, signal
