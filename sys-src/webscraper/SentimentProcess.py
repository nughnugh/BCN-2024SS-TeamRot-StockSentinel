from datetime import datetime, timedelta
import asyncio
from Database import get_unprocessed_news, update_news, cleanup_timeout
import logging
from PageCrawler import PageCrawler

logger = logging.getLogger(__name__)


class UrlInfo:
    def __init__(self, request_cnt=0, blacklisted=False):
        self.request_cnt = request_cnt
        self.blacklisted = blacklisted


class SentimentProcess:
    async def run(self):
        url_info = {}
        max_request_per_page = 200
        while True:
            news_buckets = get_unprocessed_news(10)
            logger.info(f'Page Crawl for {len(news_buckets.keys())} sources')
            for key, val in url_info.items():
                if val.blacklisted or val.request_cnt >= max_request_per_page:
                    news_buckets.pop(key, None)
            if len(news_buckets.keys()) == 0:
                break
            page_crawlers = []
            for key, pages in news_buckets.items():
                logger.info(f'Crawl {len(pages)} pages for source_id={key}')
                page_crawler = PageCrawler(pages=pages, main_url=key)
                page_crawlers.append(page_crawler)
                page_crawler.start()
            for page_crawler in page_crawlers:
                page_crawler.join()
                logger.info(f'Results for {page_crawler.main_url} pages')
                logger.info(f'Perform Update for {len(page_crawler.pages)} pages')
                update_news(page_crawler.pages)
                logger.info(f'Failure cnt: {page_crawler.failure_cnt}')
                if page_crawler.main_url not in url_info:
                    url_info[page_crawler.main_url] = UrlInfo()
                url_info[page_crawler.main_url].request_cnt += len(page_crawler.pages)
                logger.info(f'Total requests: {url_info[page_crawler.main_url].request_cnt}')
                if page_crawler.failure_cnt / float(len(page_crawler.pages)) >= 0.8:
                    url_info[page_crawler.main_url].blacklisted = True
                    logger.warning(f'Blacklist url: {page_crawler.main_url}')
            cleanup_timeout(3)
