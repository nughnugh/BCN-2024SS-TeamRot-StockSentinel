from db_setup import db_setup
import nltk

db_setup()
nltk.download('vader_lexicon')
nltk.download('punkt')

import asyncio
import logging
import sys
from datetime import datetime
from Database import DUMMY_SOURCE_STRING
from FinanceDataProcess import FinanceDataProcess
from MyFormatter import MyFormatter
from NewsProcess import NewsProcess, QueryMode, SearchParams
import os

from SentimentProcess import SentimentProcess


if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger()

fileHandler = logging.FileHandler(f"logs/crawler_{datetime.today().date()}.log")
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

FinProcess = FinanceDataProcess()
FinProcess.push_data_to_db()

special_search_params = {
    DUMMY_SOURCE_STRING: SearchParams(30, True, 20),
    "Forbes": SearchParams(30, False, 20)
}

news_crawler = NewsProcess(QueryMode.RECENT, datetime.strptime('01-01-2024', '%m-%d-%Y').date(),
                           SearchParams(30, True, 20), special_search_params)
news_crawler.run()

sentimentProcess = SentimentProcess()
asyncio.run(sentimentProcess.run())

