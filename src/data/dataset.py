"""Module used to build the dataset"""

import csv
import warnings
from math import floor

import client
from helper import get_all_usdt_symbols

warnings.filterwarnings("ignore")


def build_dataset():
    """Build dataset by downloading from Binance API"""

    # Get the current server time
    server_time = client.CLIENT.get_server_time()["serverTime"]
    for crypto_pair in get_all_usdt_symbols():
        print(crypto_pair)
        filename = "src/data/csv" + crypto_pair + ".csv"

        tmp = []

        # Get the first ever kline time
        first_kline = client.CLIENT.get_klines(
            symbol=crypto_pair,
            interval=client.CLIENT.KLINE_INTERVAL_1MINUTE,
            startTime=0,
            limit=1,
        )
        start_time = int(first_kline[0][0])
        act_time = start_time
        steps = 1000
        percentage = 0
        total_steps = server_time - start_time
        while act_time < server_time:
            current_steps = act_time - start_time + 1
            if act_time + steps > server_time:
                steps = server_time - act_time - 1
            if percentage < floor((current_steps / total_steps) * 100):
                percentage = floor((current_steps / total_steps) * 100)
                print(percentage, "% ", flush=True)
            klines = client.CLIENT.get_klines(
                symbol=crypto_pair,
                interval=client.CLIENT.KLINE_INTERVAL_1MINUTE,
                startTime=act_time,
                limit=steps,
            )
            for k in klines:
                tmp.append([k[0], k[1], k[2], k[3], k[4], k[6]])
            act_time += steps * 60000
        with open(filename, "w+", newline="") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=",")
            csv_writer.writerows(tmp)

        print(crypto_pair, " done")
