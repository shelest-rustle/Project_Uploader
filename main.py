import datetime
import logging

import config
from tk_interface import ask_open_file


def start():
    logging.info(f" Старт программы: {datetime.datetime.now()}")
    ask_open_file()


if __name__ == "__main__":
    start()
