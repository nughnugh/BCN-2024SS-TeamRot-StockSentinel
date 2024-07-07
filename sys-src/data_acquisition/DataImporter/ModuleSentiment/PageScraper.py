import json
import logging
import random
import threading
import time

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from DataImporter.common.DataModel.PageData import PageData

logger = logging.getLogger('PageScraper')


def parse_rec(json_data):
    stack = [json_data]
    iterations = 0
    while len(stack) > 0:
        if iterations > 100:
            logger.error("too many iterations: " + json_data)
            break
        elem = stack.pop()
        if type(elem) is list:
            for item in elem:
                stack.append(item)
        elif type(elem) is dict:
            if '@type' in elem:
                if elem['@type'] == 'NewsArticle':
                    return elem
            else:
                for item in elem.values():
                    stack.append(item)
        iterations += 1
    return None


def parse_meta_data(meta_data):
    for data in meta_data:
        try:
            json_data = json.loads(data.get_text())
            json_data = parse_rec(json_data)
            if json_data:
                return json_data
        except json.decoder.JSONDecodeError as e:
            logger.warning(e)
            pass
    return None


def get_meta_info(meta_data) -> (str, str, list[str]):
    item = parse_meta_data(meta_data)
    headline = ""
    description = ""
    keywords = []
    if item:
        # print(item['hasPart']['isAccessibleForFree'])
        if 'headline' in item:
            headline = item['headline']
        if 'description' in item:
            description = item['description']
        if 'keywords' in item:
            keywords = item['keywords']
    return headline, description, keywords


class PageScraper(threading.Thread):
    def __init__(self, pages: list[PageData], main_url: str, sleep_min_time: int, sleep_max_time: int):
        super().__init__()
        self.pages = pages
        headers = {
            "User-Agent": UserAgent(platforms='pc').random,
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate", # "gzip, deflate, br"
            #"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Referer": "http://www.google.com/"
        }
        self.client = requests.Session()
        self.client.headers.update(headers)
        self.main_url = main_url
        self.failure_cnt = 0
        self.sleep_min_time = sleep_min_time
        self.sleep_max_time = sleep_max_time

    def process_page(self, page: PageData) -> bool:
        try:
            response = self.client.get(page.url, timeout=(2 + page.timeout_cnt, 2 + page.timeout_cnt))
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                meta_data = soup.find_all('script', {'type': 'application/ld+json'})
                page.headline, page.description, page.keywords = get_meta_info(meta_data)
                # page.content = soup.get_text()

                text = [p.getText().strip() for p in soup.find_all(['p'])]
                page.content = "\n".join(text)

                # something probably went wrong, maybe we got blocked, try again later
                if len(page.content) < 100:
                    logger.error(f"Invalid page content: {page.content} url={page.url}")
                    page.timeout_cnt += 1
                    return False
                return True
            else:
                logger.error(f"Error fetching the page: {response.status_code} url={page.url}")
                page.timeout_cnt += 1
                self.failure_cnt += 1
        except requests.exceptions.Timeout:
            logger.error(f"Request to {page.url} timed out")
            self.failure_cnt += 1
            page.timeout_cnt += 1
        # except requests.exceptions.RequestException as e:
        #    logger.error(f"Undefined request error {e}")
        return False

    def run(self):
        for page in self.pages:
            logger.debug('fetching page: ' + page.url)
            page.success = self.process_page(page)
            time.sleep(
                self.sleep_min_time +
                random.randrange(1, 10) / 10.0 * (self.sleep_max_time - self.sleep_min_time)
            )
