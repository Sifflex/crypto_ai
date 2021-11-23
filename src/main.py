"""Main module"""

import client
from analysis import plot_sym_train_test, sum_up_data
from arguments import parse_args
from config import load_config
from dataset import build_dataset, create_pytorch_dataset, load_dataset
from helper import build_architecture

import numpy as np

if __name__ == "__main__":
    build_architecture()
    args = parse_args()

    load_config()

    if args.build_dataset:
        build_dataset()

    dataset = load_dataset()

    split_ratio = 0.7

    if args.plot:
        plot_dataset = sum_up_data(dataset, args.plot, "1MIN")
        plot_sym_train_test(plot_dataset, split_ratio)
