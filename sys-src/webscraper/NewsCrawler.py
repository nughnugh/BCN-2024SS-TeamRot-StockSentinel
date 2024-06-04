from datetime import datetime, timedelta
from time import sleep

from Database import get_all_stocks, get_all_news_sources, insert_stock_news_batch, remove_existing_news, \
    get_news_time_span
from GoogleCrawler import GoogleCrawler


class QueryMode:
    RECENT = 1
    HISTORY = 2


class NewsCrawler:
    def __init__(self, query_mode, history_min_date, agg_days):
        self.query_mode = query_mode
        self.history_min_date = history_min_date
        self.agg_days = agg_days

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
                min_date, max_date = get_news_time_span(stock, source)
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
                    print(f"work dates not filled")
                    continue

                print(f"Total range {work_min_date} to {work_max_date}")

                while work_min_date < work_max_date:
                    start_date = max(work_max_date - timedelta(days=self.agg_days), work_min_date)
                    print(f"Work range {start_date} to {work_max_date}")

                    google_crawler = GoogleCrawler(stock=stock, existing_sources=existing_sources,
                                                   search_time_start=start_date, search_time_end=work_max_date,
                                                   source=source, search_by_ticker=False)

                    stock_news = google_crawler.run()
                    prev_cnt = len(stock_news)
                    stock_news = remove_existing_news(stock_news)
                    print(f"crawled {len(stock_news)} new articles ({prev_cnt} total)")
                    insert_stock_news_batch(stock_news)
                    work_max_date = start_date - timedelta(days=1)
                    sleep(2.5)

            # googleCrawler = GoogleCrawler(stock, existing_sources, 'd', 7, search_by_ticker=True)
            # insert_stock_news_batch(stock_news)
