import requests
import pandas as pd

from config import (
    SYMBOL,
    INTERVAL,
    LIMIT,
    FAST_EMA,
    SLOW_EMA,
    SIGNAL_EMA,
    EMA_FILTER,
)

URL = "https://api.binance.com/api/v3/klines"


def get_dataframe():

    response = requests.get(
        URL,
        params={
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "limit": LIMIT,
        },
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    df = pd.DataFrame(
        data,
        columns=[
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_base",
            "taker_buy_quote",
            "ignore",
        ],
    )

    df["close"] = df["close"].astype(float)

    return df


def calculate():

    df = get_dataframe()

    ema12 = df["close"].ewm(
        span=FAST_EMA,
        adjust=False
    ).mean()

    ema26 = df["close"].ewm(
        span=SLOW_EMA,
        adjust=False
    ).mean()

    macd = ema12 - ema26

    signal = macd.ewm(
        span=SIGNAL_EMA,
        adjust=False
    ).mean()

    ema200 = df["close"].ewm(
        span=EMA_FILTER,
        adjust=False
    ).mean()

    return df, macd, signal, ema200
