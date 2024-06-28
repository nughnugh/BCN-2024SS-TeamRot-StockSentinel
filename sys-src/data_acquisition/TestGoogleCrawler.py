import logging
import sys
from datetime import datetime

from DataImporter.common.Database.Database import get_all_stocks, get_all_news_sources
from DataImporter.ModuleNews import GoogleCrawler
from DataImporter.common.misc.MyFormatter import MyFormatter

stock_list = get_all_stocks()
source_list = get_all_news_sources()
existing_sources = {}
for source in source_list:
    existing_sources[source.url] = source

logger = logging.getLogger()

consoleHandler = logging.StreamHandler(stream=sys.stdout)
consoleHandler.setFormatter(MyFormatter(True))
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)
logger.setLevel(logging.DEBUG)

print(stock_list[9].name)
print(source_list[0].name)

google_crawler = GoogleCrawler(stock=stock_list[9], existing_sources=existing_sources,
                               search_time_start=datetime.strptime('01-01-2024', '%m-%d-%Y').date(),
                               search_time_end=datetime.strptime('06-06-2024', '%m-%d-%Y').date(),
                               source=source_list[0], search_by_ticker=False)
pages = google_crawler.run()
for page in pages:
    print(page.url)