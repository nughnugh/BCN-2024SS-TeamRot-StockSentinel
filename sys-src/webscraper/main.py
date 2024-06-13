import asyncio
import logging
import sys
from datetime import datetime
import nltk

from MyFormatter import MyFormatter
from NewsProcess import NewsProcess, QueryMode
import os

from SentimentProcess import SentimentProcess

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

logger.info(f"=======================================")
logger.info(f"Start process: {datetime.now()}")
logger.info(f"=======================================")

news_crawler = NewsProcess(QueryMode.RECENT, datetime.strptime('01-01-2024', '%m-%d-%Y').date(), 7)
news_crawler.run()

sentimentProcess = SentimentProcess()
asyncio.run(sentimentProcess.run())
