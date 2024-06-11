from datetime import datetime, timedelta
import asyncio
from Database import get_unprocessed_news, update_news
import logging
from PageCrawler import PageCrawler

logger = logging.getLogger(__name__)

class SentimentProcess:


    async def run(self):
        while True:
            news = get_unprocessed_news(10)
            all_tasks = []
            logger.info(f'Page Crawl for {len(news.keys())} sources')
            if news.keys() == 0:
                break
            for key in news.keys():
                logger.info(f'Crawl {len(news[key])} pages for source_id={key}')
                pages = news[key]
                page_crawler = PageCrawler(pages=pages)
                task = asyncio.create_task(page_crawler.get_content())
                all_tasks.append(task)
            for task in all_tasks:
                processed_pages = await task
                logger.info(f'Perform Update for {len(processed_pages)} pages')
                update_news(processed_pages)
