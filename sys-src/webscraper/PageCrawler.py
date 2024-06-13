import asyncio
import logging
import random
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from PageData import PageData
from SentAnalyzer import analyze

logger = logging.getLogger(__name__)

#logger = logging.getLogger(__name__)

class PageCrawler:
    def __init__(self, pages: list[PageData]):
        self.pages = pages
        headers = {"User-Agent": UserAgent(platforms='pc').random}
        self.client = requests.Session()
        self.client.headers.update(headers)

    async def get_content(self) -> list[PageData]:
        sentiment_tasks = []
        error_pages = []
        for page in self.pages:
            try:
                response = self.client.get(page.url, timeout=(2,2))
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    page.content = soup.get_text()
                    task = asyncio.create_task(analyze(page))
                    sentiment_tasks.append(task)
                    await asyncio.sleep(0.5 + random.randrange(1, 5) / 10.0)
                else:
                    logger.error(f"Error fetching the page: {response.status_code}")
                    page.timeout = True
                    error_pages.append(page)
            except requests.exceptions.Timeout:
                logger.error(f"Request to {page.url} timed out")
                page.timeout = True
                error_pages.append(page)
            except requests.exceptions.RequestException as e:
                logger.error(f"Undefined request error {e}")
                page.timeout = True
                error_pages.append(page)
        new_pages = error_pages
        for task in sentiment_tasks:
            new_pages.append(await task)

    async def process_page(self, page: PageData) -> PageData:
        try:
            response = self.client.get(page.url, timeout=(2 + page.timeout_cnt, 2 + page.timeout_cnt))
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                page.content = soup.get_text()
                page = analyze(page)
            else:
                logger.error(f"Error fetching the page: {response.status_code}")
                page.timeout_cnt += 1
        except requests.exceptions.Timeout:
            logger.error(f"Request to {page.url} timed out")
            page.timeout_cnt += 1
        # except requests.exceptions.RequestException as e:
        #    logger.error(f"Undefined request error {e}")
        return page

    async def get_content(self) -> list[PageData]:
        tasks = []
        for page in self.pages:
            task = self.process_page(page)
            tasks.append(task)
            await asyncio.sleep(0.5 + random.randrange(1, 5) / 10.0)
        new_pages = []
        for task in tasks:
            new_pages.append(await task)
        return new_pages
