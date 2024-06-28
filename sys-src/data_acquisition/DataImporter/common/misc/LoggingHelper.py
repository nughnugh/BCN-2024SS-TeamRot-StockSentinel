import logging
import os
import sys
from datetime import datetime

from DataImporter.common.misc.MyFormatter import MyFormatter


def init_logger(module_name):
    if not os.path.exists(f"logs/{module_name}"):
        os.makedirs(f"logs/{module_name}")

    logger = logging.getLogger()

    fileHandler = logging.FileHandler(f"logs/{module_name}/crawler_{module_name}_{datetime.today().date()}.log")
    fileHandler.setFormatter(MyFormatter(False))
    fileHandler.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler(stream=sys.stdout)
    consoleHandler.setFormatter(MyFormatter(True))
    consoleHandler.setLevel(logging.INFO)

    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
    logger.setLevel(logging.DEBUG)

    logger.info(f"=======================================")
    logger.info(f"Start process: {datetime.now()}")
    logger.info(f"=======================================")
