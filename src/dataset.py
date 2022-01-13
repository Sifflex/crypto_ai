"""Module used to build the dataset"""

import csv
import warnings
from pathlib import Path

import math
import numpy as np
import pandas as pd
from plotly.graph_objs import Candlestick, Figure

import client
from client import get_all_usdt_symbols
from logger import log

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
    for interval in intervals:
        for symbol in get_all_usdt_symbols():
            path = Path(
                "data",
                "csv",
                (
                    "1MIN_"
                    if interval == client.CLIENT.KLINE_INTERVAL_1MINUTE
                    else "15MIN_"
                )
                + symbol
                + ".csv",
            )

            if path.exists():
                continue

            log(f"Downloading data for {symbol}")
            tmp = []

            # Get the first ever kline time
            first_kline = client.CLIENT.get_klines(
                symbol=symbol, interval=interval, startTime=0, limit=1
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
                    symbol=symbol, interval=interval, startTime=act_time, limit=steps
                )
                for k in klines:
                    tmp.append([k[0], k[1], k[2], k[3], k[4], k[6]])
                act_time += (
                    steps
                    * 1000
                    * 60
                    * (1 if interval == client.CLIENT.KLINE_INTERVAL_1MINUTE else 15)
                )
            with open(path, "w+", newline="") as csvfile:
                csv_writer = csv.writer(csvfile, delimiter=",")
                csv_writer.writerows(tmp)

            print("100 %")
            print(symbol, " done")

def load_dataset():
    """Load all csv files into one dataframe with 3 levels"""

    csv_folder = Path("data", "csv")
    col_names = ["open time", "open", "high", "low", "close", "close time"]
    intervals = ["1MIN", "15MIN"]
    symbols = get_all_usdt_symbols()[:1]

    df = pd.DataFrame()
    current_symbol = 0
    total_symbols = len(symbols)
    for symbol in symbols:
        print(f"{round((current_symbol / total_symbols) * 100, 1)} %", end="\r")
        for interval in intervals:
            symbol_interval_path = csv_folder / f"{interval}_{symbol}.csv"
            sub_df = pd.read_csv(symbol_interval_path, names=col_names)
            sub_df["symbol"] = symbol
            sub_df["interval"] = interval
            df = df.append(sub_df)
        current_symbol += 1
    print('100%      ')


    df = df.set_index(["symbol", "interval", "open time"])
    df = df.sort_index(level=0, ascending=True)

    df["open"] = df["open"].astype("float32")
    df["high"] = df["high"].astype("float32")
    df["low"] = df["low"].astype("float32")
    df["close"] = df["close"].astype("float32")
    del df["close time"]

    return df

def split_train_test_val(df, symbol, interval, test_ratio=0.2, validation_ratio=0.2):
    train_ratio = 1.0 - test_ratio - validation_ratio
    open_times = df.loc[symbol, interval, :].index.get_level_values(2).unique().to_numpy(dtype=np.uint64)
    train_test_date_split = open_times[math.floor(open_times.shape[0] * train_ratio)]
    test_validation_date_split = open_times[math.floor(open_times.shape[0] * (train_ratio + test_ratio))]
    print(df.shape)
    train = df.loc[:, :, :train_test_date_split]
    test = df.loc[:, :, train_test_date_split:test_validation_date_split]
    validation = df.loc[:, :, test_validation_date_split:]
    print(train.shape, test.shape, validation.shape)
    return (train, test, validation)