"""Helpers functions module"""

from plotly.graph_objs import Candlestick

import client
import config


def get_all_usdt_symbols():
    """Return all existing symbols related to USDT that are not blacklisted"""

    symbols = []

    data = client.CLIENT.get_exchange_info()

    for sym in data["symbols"]:

        symbol = sym["symbol"]

        if (
            "blacklisted_symbols" in config.CONFIG
            and symbol in config.CONFIG["blacklisted_symbols"]
        ):
            continue

        if symbol.endswith("USDT"):
            if (
                not symbol.endswith("UPUSDT")
                and not symbol.endswith("BULLUSDT")
                and not symbol.endswith("DOWNUSDT")
                and not symbol.endswith("BEARUSDT")
            ):
                symbols.append(symbol)

    return symbols


def plot_train_test(train, test):
    data = [
        Candlestick(
            x=train.index,
            open=train["Open"],
            high=train["High"],
            low=train["Low"],
            close=train["Close"],
            name="train",
        ),
        Candlestick(
            x=test.index,
            open=test["Open"],
            high=test["High"],
            low=test["Low"],
            close=test["Close"],
            name="test",
        ),
    ]

    return data
