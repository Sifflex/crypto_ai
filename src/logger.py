"""Logger module"""

import datetime

from helper import get_time

LOGS_PATH = "data/logs"


def log(data):
    """Write to file and in terminal"""

    now = datetime.datetime.fromtimestamp(get_time() / 1000)

    data = now.strftime("%Y-%m-%d %H:%M:%S") + " - " + data

    print(data)
    with open(LOGS_PATH, "a") as log_file:
        log_file.write(data + "\n")
