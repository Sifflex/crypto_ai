"""Module used to store the client variable used to interact with Binance"""

from binance.client import Client

import config

CLIENT = None


def load_client():
    """Make global_client a global variable"""

    global CLIENT
    CLIENT = Client(config.CONFIG["API_KEY"], config.CONFIG["API_SECRET"])
    