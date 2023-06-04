import logging
import sys


def init_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    std_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

    std_handler.setFormatter(formatter)

    logger.addHandler(std_handler)

    return logger
