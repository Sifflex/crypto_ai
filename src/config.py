"""Module used to load a configuration file"""

import sys
from pathlib import Path

import yaml

CONFIG = None


def load_config():
    """Make CONFIG a global variable"""

    global CONFIG
    config_path = "config.yml"
    if Path(config_path).is_file():
        with open(config_path) as config_file:
            CONFIG = yaml.safe_load(config_file)
            print(CONFIG)
    else:
        print(f"No config file found ({config_path})")
        sys.exit(1)
