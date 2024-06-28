print("hello my friends!")

"""
db_setup()
nltk.download('vader_lexicon')
nltk.download('punkt')

import asyncio
import logging
import sys
from datetime import datetime
from Database.Database import DUMMY_SOURCE_STRING
from misc.MyFormatter import MyFormatter
from ModuleNews.NewsProcess import SearchParams, NewsProcess, QueryMode
import os

from ModuleSentiment.SentimentProcess import SentimentProcess
from ModuleFinance.FinanceDataProcess import FinanceDataProcess

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


fin_process = FinanceDataProcess()
fin_process.start()


special_search_params = {
    DUMMY_SOURCE_STRING: SearchParams(30, True, 20),
    "Forbes": SearchParams(30, False, 20)
}

news_crawler = NewsProcess(QueryMode.HISTORY, datetime.strptime('01-01-2024', '%m-%d-%Y').date(),
                           SearchParams(30, True, 20), special_search_params, pause_time=0.1)
news_crawler.run()

sentimentProcess = SentimentProcess(0.3, 1)
asyncio.run(sentimentProcess.run())
"""