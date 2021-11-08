"""Main module"""

from arguments import parse_args
from config import load_config
from dataset import build_dataset
from helper import build_architecture

if __name__ == "__main__":

    build_architecture()
    args = parse_args()

    load_config()

    if args.build_dataset:
        build_dataset()
