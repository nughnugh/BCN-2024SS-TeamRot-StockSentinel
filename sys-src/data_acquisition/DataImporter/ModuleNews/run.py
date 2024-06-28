from datetime import datetime
from .NewsProcess import SearchParams, NewsProcess, QueryMode
from DataImporter.common.Database.Database import DUMMY_SOURCE_STRING
from DataImporter.common.misc.LoggingHelper import init_logger

if __name__ == '__main__':
    init_logger('NewsProcess')
    special_search_params = {
        DUMMY_SOURCE_STRING: SearchParams(30, True, 20),
        "Forbes": SearchParams(30, False, 20)
    }

    news_crawler = NewsProcess(QueryMode.RECENT, datetime.strptime('01-01-2024', '%m-%d-%Y').date(),
                               SearchParams(30, True, 20), special_search_params, pause_time=0.1)
    news_crawler.run()
