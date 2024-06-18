import asyncio
import logging
import sys
from datetime import datetime
import nltk

from Database import DUMMY_SOURCE_STRING
from MyFormatter import MyFormatter
from NewsProcess import NewsProcess, QueryMode, SearchParams
import os

from SentimentProcess import SentimentProcess
from db_setup import db_setup

nltk.download('vader_lexicon')
nltk.download('punkt')

if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger()

fileHandler = logging.FileHandler(f"logs/crawler_{datetime.today().date()}.log")
fileHandler.setFormatter(MyFormatter(False))

consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setFormatter(MyFormatter(True))

logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

logger.setLevel(logging.INFO)

db_setup()

logger.info(f"=======================================")
logger.info(f"Start process: {datetime.now()}")
logger.info(f"=======================================")

special_search_params = {
    DUMMY_SOURCE_STRING: SearchParams(7, True)
}
news_crawler = NewsProcess(QueryMode.RECENT, datetime.strptime('01-01-2024', '%m-%d-%Y').date(),
                           SearchParams(30, False), special_search_params)
news_crawler.run()

sentimentProcess = SentimentProcess()
asyncio.run(sentimentProcess.run())
