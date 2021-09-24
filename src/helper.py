"""Helpers functions module"""

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
