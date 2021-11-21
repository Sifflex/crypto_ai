import math

import numpy as np
import pandas as pd
from plotly.graph_objs import Candlestick, Figure

import client


def sum_up_data(df, symbol, interval):
    switch = {
        '1MIN': 15000,
        '15MIN': 1000,
    }
    ratio = switch.get(interval, 10000)
    values = df.loc[symbol, interval, :].index.get_level_values(2).unique().to_numpy(dtype=np.uint64)
    res = np.empty([0, 5])
    for i in range(0, values.shape[0], ratio):
        tmp = df.loc[symbol, interval, values[i]:values[min(i + ratio - 1, len(values) - 1)]]
        to_add = np.array(
                [
                    values[i],
                    tmp.iloc[0]["open"],
                    tmp["low"].min(),
                    tmp["high"].max(),
                    tmp.iloc[-1]["close"]
                ]
        )
        print(f"{round((i / values.shape[0]) * 100, 1)} %", end="\r")
        res = np.vstack((res, to_add))
    return pd.DataFrame(
        res,
        columns=[
            "Open Time",
            "Open",
            "High",
            "Low",
            "Close",
        ],
    )

def plot_sym_train_test(df, split_ratio):
    df_copy = df.copy()
    print(df)
    df_copy["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
    df_copy["Open"] = df_copy["Open"].apply(math.log2)
    df_copy["Close"] = df_copy["Close"].apply(math.log2)
    df_copy["High"] = df_copy["High"].apply(math.log2)
    df_copy["Low"] = df_copy["Low"].apply(math.log2)
    date_split = df_copy["Open Time"][math.floor(df_copy.shape[0] * split_ratio)]
    data = [
        Candlestick(
            x=df_copy["Open Time"],
            open=df_copy["Open"],
            high=df_copy["High"],
            low=df_copy["Low"],
            close=df_copy["Close"],
            name="df_copy",
        )
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
