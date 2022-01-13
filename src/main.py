"""Main module"""

import client
from analysis import plot_sym_train_test, sum_up_data
from arguments import parse_args
from config import load_config
from dataset import build_dataset, load_dataset, split_train_test_val
from helper import build_architecture

import numpy as np

if __name__ == "__main__":
    build_architecture()
    args = parse_args()

    load_config()

    if args.build_dataset:
        build_dataset()

    dataset = load_dataset()
    train, test, validation = split_train_test_val(dataset, 'BTCUSDT', '1MIN')

    if args.plot:
        plot_dataset = sum_up_data(dataset, args.plot, "1MIN")
        plot_sym_train_test(plot_dataset)
