from datetime import datetime, timedelta
from time import sleep

from DataImporter.common.Database.Database import get_all_stocks, get_all_news_sources, insert_stock_news_batch, \
    remove_existing_news, get_news_time_span
from .GoogleCrawler import GoogleCrawler

import logging

logger = logging.getLogger(__name__)


class QueryMode:
    RECENT = 1
    HISTORY = 2


class SearchParams:
    def __init__(self, agg_days: int = 7, ticker_related: bool = False, max_cnt_per_agg: int = 10):
        self.agg_days = agg_days
        self.ticker_related = ticker_related
        self.max_cnt_per_agg = max_cnt_per_agg


class NewsProcess:
    def __init__(self, query_mode, history_min_date, def_search_params: SearchParams,
                 source_search_params: dict[str, SearchParams] = None, pause_time=0.5):
        self.query_mode = query_mode
        self.history_min_date = history_min_date
        self.def_search_params = def_search_params
        self.source_search_params = {}
        self.pause_time = pause_time
        if source_search_params:
            self.source_search_params = source_search_params

    def run(self):
        stock_list = get_all_stocks()
        source_list = get_all_news_sources()
        existing_sources = {}
        for source in source_list:
            existing_sources[source.url] = source

        for stock in stock_list:
            for source in source_list:
                work_min_date = None
                work_max_date = None
                if source.name in self.source_search_params:
                    search_params = self.source_search_params[source.name]
                else:
                    search_params = self.def_search_params

                min_date, max_date = get_news_time_span(stock, source, search_params.ticker_related)

                if self.query_mode == QueryMode.HISTORY:
                    if not min_date:
                        work_min_date = self.history_min_date
                        work_max_date = datetime.today().date()
                    elif self.history_min_date < min_date.date():
                        work_min_date = self.history_min_date
                        work_max_date = min_date.date()
                elif self.query_mode == QueryMode.RECENT:
                    if not max_date:
                        work_min_date = self.history_min_date
                        work_max_date = datetime.today().date()
                    elif max_date.date() < datetime.today().date():
                        work_min_date = max_date.date()
                        work_max_date = datetime.today().date()

                if not work_min_date or not work_max_date:
                    logger.info(f"News all up to date")
                    continue

                logger.info(f"Total range {work_min_date} to {work_max_date}")

                while work_min_date < work_max_date:
                    start_date = max(work_max_date - timedelta(days=search_params.agg_days), work_min_date)
                    logger.info(f"Work range {start_date} to {work_max_date}")

                    google_crawler = GoogleCrawler(stock=stock, existing_sources=existing_sources,
                                                   search_time_start=start_date, search_time_end=work_max_date,
                                                   source=source, search_by_ticker=search_params.ticker_related)

                    stock_news = google_crawler.run()
                    stock_news = stock_news[:search_params.max_cnt_per_agg]
                    prev_cnt = len(stock_news)
                    stock_news = remove_existing_news(stock_news)
                    insert_stock_news_batch(stock_news)
                    logger.info(f"inserted {len(stock_news)} new articles ({prev_cnt} total)")
                    work_max_date = start_date - timedelta(days=1)
                    sleep(self.pause_time)
