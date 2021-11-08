"""Helper functions module"""

import datetime
from pathlib import Path


def build_architecture():
    """Build the project's architecture"""

    dataset_dir = Path("data", "csv")
    dataset_dir.mkdir(parents=True, exist_ok=True)


def get_time():
    """Return current timestamp"""

    return int(datetime.datetime.now().timestamp() * 1000)
