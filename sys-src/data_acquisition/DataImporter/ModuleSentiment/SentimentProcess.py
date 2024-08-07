import threading

from DataImporter.common.Database.Database import get_unprocessed_news, update_news, cleanup_timeout, unlock_stock_news
import logging
from .PageScraper import PageScraper
from .SentAnalyzer import analyze, tokenize

logger = logging.getLogger('SentProcess')

class UrlInfo:
    def __init__(self, request_cnt=0, blacklisted=False):
        self.request_cnt = request_cnt
        self.blacklisted = blacklisted


class SentimentProcess():
    def __init__(self, sleep_min_time=1, sleep_max_time=2):
        self.sleep_min_time = sleep_min_time
        self.sleep_max_time = sleep_max_time
        self.running = False
        self.news_buckets = {}
        self.page_scrapers = []

    def run(self):
        url_info = {}
        max_request_per_page = 400
        self.running = True
        while self.running:
            self.news_buckets = get_unprocessed_news(10)
            logger.info(f'Page Crawl for {len(self.news_buckets.keys())} sources')
            for key, val in url_info.items():
                if val.blacklisted or val.request_cnt >= max_request_per_page:
                    self.news_buckets.pop(key, None)
            if len(self.news_buckets.keys()) == 0:
                break
            self.page_scrapers = []
            for key, pages in self.news_buckets.items():
                logger.info(f'Crawl {len(pages)} pages for source_id={key}')
                page_scraper = PageScraper(pages, key, self.sleep_min_time, self.sleep_max_time)
                self.page_scrapers.append(page_scraper)
                page_scraper.start()
            for page_scraper in self.page_scrapers:
                page_scraper.join()

                common_sentences = {}
                for page in page_scraper.pages:
                    if page.success:
                        page.sentences = tokenize(page.content)
                        for sentence in page.sentences:
                            if sentence not in common_sentences:
                                common_sentences[sentence] = 0
                            common_sentences[sentence] += 1
                for page in page_scraper.pages:
                    if page.success:
                        filtered_sentences = []
                        for sentence in page.sentences:
                            if common_sentences[sentence] <= 1:
                                filtered_sentences.append(sentence)
                        page.sentences = filtered_sentences
                        analyze(page)
                        page.content = '\n'.join(page.sentences)
                logger.info(f'Results for {page_scraper.main_url} pages')
                logger.info(f'Perform Update for {len(page_scraper.pages)} pages')
                update_news(page_scraper.pages)
                logger.info(f'Failure cnt: {page_scraper.failure_cnt}')
                if page_scraper.main_url not in url_info:
                    url_info[page_scraper.main_url] = UrlInfo()
                url_info[page_scraper.main_url].request_cnt += len(page_scraper.pages)
                logger.info(f'Total requests: {url_info[page_scraper.main_url].request_cnt}')
                if page_scraper.failure_cnt / float(len(page_scraper.pages)) >= 0.8 and len(page_scraper.pages) >= 4:
                    url_info[page_scraper.main_url].blacklisted = True
                    logger.warning(f'Blacklist url: {page_scraper.main_url}')
            cleanup_timeout(3)

    def stop(self, signal, frame):
        logger.info("Shutdown process...")
        self.running = False
        all_pages = []
        for key, pages in self.news_buckets.items():
            all_pages.extend(pages)
        unlock_stock_news(all_pages)
        logger.info(f"Unlock {len(all_pages)} pages")

        logger.info("Shutdown complete.")
