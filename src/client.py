"""Module used to store the client variable used to interact with Binance"""

from binance.client import Client

import config

CLIENT = None


def _load_client():
    """Make global_client a global variable"""

    global CLIENT
    if not CLIENT:
        print("Initializing client")
        CLIENT = Client(config.CONFIG["API_KEY"], config.CONFIG["API_SECRET"])


def get_all_usdt_symbols():
    """Return all existing symbols related to USDT that are not blacklisted"""

    _load_client()

    symbols = []
    data = CLIENT.get_exchange_info()
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
