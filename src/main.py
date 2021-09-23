"""Main module"""

from arguments import parse_args
from client import load_client
from config import load_config
from data.dataset import build_dataset

if __name__ == "__main__":
    args = parse_args()

    load_config()
    load_client()


    if args.build_dataset:
        build_dataset()
