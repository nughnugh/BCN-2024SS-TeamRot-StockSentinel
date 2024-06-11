import logging
from datetime import datetime
import nltk
from NewsCrawler import NewsCrawler, QueryMode
import os

nltk.download('vader_lexicon')
nltk.download('punkt')

if not os.path.exists("logs"):
    os.makedirs("logs")

logger = logging.getLogger()
logFormatter = logging.Formatter("%(asctime)s [%(name)-12.12s] [%(levelname)-5.5s]  %(message)s")

fileHandler = logging.FileHandler(f"logs/crawler_{datetime.today().date()}.log")
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

logger.setLevel(logging.INFO)

logger.info(f"=======================================")
logger.info(f"Start process: {datetime.now()}")
logger.info(f"=======================================")

news_crawler = NewsCrawler(QueryMode.RECENT, datetime.strptime('01-01-2024', '%m-%d-%Y').date(), 7)
news_crawler.run()
