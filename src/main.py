"""Main module"""

import client
from analysis import plot_sym_train_test, sum_up_data
from arguments import parse_args
from config import load_config
from data.dataset import build_dataset, create_pytorch_dataset

if __name__ == "__main__":
    args = parse_args()

    load_config()
    client.load_client()

    if args.build_dataset:
        build_dataset()

    (train, test) = create_pytorch_dataset(
        "ADAUSDT", client.CLIENT.KLINE_INTERVAL_1MINUTE
    )

    if args.plot:
        show_train = sum_up_data(train, client.CLIENT.KLINE_INTERVAL_1MINUTE)
        show_test = sum_up_data(test, client.CLIENT.KLINE_INTERVAL_1MINUTE)
        plot_sym_train_test(show_train, show_test)
