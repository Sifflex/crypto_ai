"""Main module"""

from arguments import parse_args
from config import load_config
from dataset import (
    build_dataset,
    create_pytorch_dataset,
    load_dataset,
    plot_sym_train_test,
)

if __name__ == "__main__":
    args = parse_args()

    load_config()

    if args.build_dataset:
        build_dataset()

    # (train, test) = create_pytorch_dataset(
    #     "ADAUSDT", client.CLIENT.KLINE_INTERVAL_1MINUTE
    # )
    # plot_sym_train_test(train=train, test=test)
