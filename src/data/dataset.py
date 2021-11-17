"""Module used to build the dataset"""

import csv
import warnings
from pathlib import Path

import pandas as pd
from plotly.graph_objs import Candlestick, Figure

import client
from helper import get_all_usdt_symbols

warnings.filterwarnings("ignore")


def build_dataset():
    """Build dataset by downloading from Binance API"""
    # Kline intervals we will be working with
    intervals = [
        client.CLIENT.KLINE_INTERVAL_1MINUTE,
        client.CLIENT.KLINE_INTERVAL_15MINUTE,
    ]

    # Get the current server time
    server_time = client.CLIENT.get_server_time()["serverTime"]
    for it in intervals:
        for cp in get_all_usdt_symbols():
            path = Path(
                "src",
                "data",
                "csv",
                ("1MIN" if it == client.CLIENT.KLINE_INTERVAL_1MINUTE else "15MIN")
                + cp
                + ".csv",
            )

            if path.exists():
                continue

            print(cp)
            tmp = []

            # Get the first ever kline time
            first_kline = client.CLIENT.get_klines(
                symbol=cp, interval=it, startTime=0, limit=1
            )
            start_time = int(first_kline[0][0])
            act_time = start_time
            steps = 1000
            total_steps = server_time - start_time
            while act_time < server_time:
                current_steps = act_time - start_time
                if act_time + steps > server_time:
                    steps = server_time - act_time - 1
                print(f"{round((current_steps / total_steps) * 100, 1)} %", end="\r")
                klines = client.CLIENT.get_klines(
                    symbol=cp, interval=it, startTime=act_time, limit=steps
                )
                for k in klines:
                    """
                    0: Open time
                    1: Open
                    2: High
                    3: Low
                    4: Close
                    6: Close time
                    """
                    tmp.append([k[0], k[1], k[2], k[3], k[4], k[6]])
                act_time += (
                    steps
                    * 1000
                    * 60
                    * (1 if it == client.CLIENT.KLINE_INTERVAL_1MINUTE else 15)
                )
            with open(path, "w+", newline="") as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=",")
                csv_writer.writerows(tmp)

            print("100 %")
            print(cp, " done")


def create_pytorch_dataset(symbol, interval, split_ratio=0.7):
    """Build a pytorch dataset based on the input symbol"""

    str_interval = (
        "1MIN" if interval == client.CLIENT.KLINE_INTERVAL_1MINUTE else "15MIN"
    )
    btc_names = [
        "BTC Open Time",
        "BTC Open",
        "BTC High",
        "BTC Low",
        "BTC Close",
        "BTC Close Time",
    ]
    sym_names = ["Open Time", "Open", "High", "Low", "Close", "Close time"]
    btc_df = pd.read_csv(
        "src/data/csv/" + str_interval + "BTCUSDT.csv", names=btc_names
    )
    sym_df = pd.read_csv(
        "src/data/csv/" + str_interval + symbol + ".csv", names=sym_names
    )

    # Resizing the dataframes in order to have the same first Open Time
    open_btc = btc_df["BTC Open Time"][0]
    open_sym = sym_df["Open Time"][0]
    if open_btc < open_sym:
        btc_df = btc_df[(open_sym - open_btc) // 60000 :]
        btc_df = btc_df.reset_index()
        btc_df = btc_df.drop("index", 1)
    elif open_btc != open_sym:
        sym_df = sym_df[(open_btc - open_sym) // 60000 :]
        sym_df = sym_df.reset_index()
        sym_df = sym_df.drop("index", 1)

    # Same for the last Open Time
    len_btc_df = len(btc_df)
    len_sym_df = len(sym_df)
    if len_btc_df < len_sym_df:
        sym_df = sym_df[:len_btc_df]
    else:
        btc_df = btc_df[:len_sym_df]

    btc_sym_df = btc_df.join(sym_df)
    btc_sym_df = btc_sym_df.drop("BTC Open Time", 1)
    btc_sym_df = btc_sym_df.drop("BTC Close Time", 1)
    btc_sym_df = btc_sym_df[
        [
            "Open Time",
            "BTC Open",
            "BTC High",
            "BTC Low",
            "BTC Close",
            "Open",
            "High",
            "Low",
            "Close",
            "Close time",
        ]
    ]

    index_split = int(len(btc_sym_df) * split_ratio)
    train = btc_sym_df[:index_split]
    test = btc_sym_df[index_split:]
    return (train, test)


def plot_sym_train_test(train, test):
    data = [
        Candlestick(
            x=train["Open Time"],
            open=train["Open"],
            high=train["High"],
            low=train["Low"],
            close=train["Close"],
            name="train",
        ),
        Candlestick(
            x=test["Open Time"],
            open=test["Open"],
            high=test["High"],
            low=test["Low"],
            close=test["Close"],
            name="test",
        ),
    ]

    figure = Figure(data=data)
    figure.show()
