import math

import numpy as np
import pandas as pd
from plotly.graph_objs import Candlestick, Figure

import client


def sum_up_data(df, kline_interval):
    switch = {
        client.CLIENT.KLINE_INTERVAL_1MINUTE: 1500,
        client.CLIENT.KLINE_INTERVAL_15MINUTE: 100,
    }
    ratio = switch.get(kline_interval, 10000)

    res = np.empty([0, 10])
    for i in range(0, df.shape[0], ratio):
        tmp = df[i : i + ratio].to_numpy()
        lowest_btc = math.inf
        lowest_coin = math.inf
        highest_btc = 0
        highest_coin = 0
        for j in range(0, tmp.shape[0]):
            lowest_btc = lowest_btc if lowest_btc < tmp[j][3] else tmp[j][3]
            lowest_coin = lowest_coin if lowest_coin < tmp[j][6] else tmp[j][6]
            highest_btc = highest_btc if highest_btc > tmp[j][2] else tmp[j][2]
            highest_coin = highest_coin if highest_coin > tmp[j][5] else tmp[j][5]
        to_add = np.array(
            [
                tmp[0][0],
                tmp[0][1],
                highest_btc,
                lowest_btc,
                tmp[tmp.shape[0] - 1][4],
                tmp[0][5],
                highest_coin,
                lowest_coin,
                tmp[tmp.shape[0] - 1][8],
                tmp[tmp.shape[0] - 1][9],
            ]
        )
        res = np.vstack((res, to_add))
    return pd.DataFrame(
        res,
        columns=[
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
        ],
    )


def plot_sym_train_test(train, test):
    train_copy = train.copy()
    test_copy = test.copy()
    train_copy["Open Time"] = pd.to_datetime(train["Open Time"], unit="ms")
    test_copy["Open Time"] = pd.to_datetime(test["Open Time"], unit="ms")
    date_split = test["Open Time"][0]
    data = [
        Candlestick(
            x=train_copy["Open Time"],
            open=train_copy["Open"],
            high=train_copy["High"],
            low=train_copy["Low"],
            close=train_copy["Close"],
            name="train_copy",
        ),
        Candlestick(
            x=test_copy["Open Time"],
            open=test_copy["Open"],
            high=test_copy["High"],
            low=test_copy["Low"],
            close=test_copy["Close"],
            name="test_copy",
        ),
    ]

    layout = {
        "shapes": [
            {
                "x0": date_split,
                "x1": date_split,
                "y0": 0,
                "y1": 1,
                "xref": "x",
                "yref": "paper",
                "line": {"color": "rgb(0,0,0)", "width": 1},
            }
        ],
        "annotations": [
            {
                "x": date_split,
                "y": 1.0,
                "xref": "x",
                "yref": "paper",
                "showarrow": False,
                "xanchor": "left",
                "text": " test data",
            },
            {
                "x": date_split,
                "y": 1.0,
                "xref": "x",
                "yref": "paper",
                "showarrow": False,
                "xanchor": "right",
                "text": "train data ",
            },
        ],
    }

    figure = Figure(data=data, layout=layout)
    figure.show()
