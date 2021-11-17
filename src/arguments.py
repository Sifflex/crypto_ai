"""Module used to parse arguments"""

import argparse


def parse_args():
    """Parse command line arguments and return them"""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--build-dataset",
        dest="build_dataset",
        action="store_true",
        help="build dataset from Binance API",
    )

    parser.add_argument(
        "--plot",
        dest="plot",
        action="store_true",
        help="plot a certain symbol",
    )

    return parser.parse_args()
