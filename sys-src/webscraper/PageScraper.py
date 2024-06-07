import random
import time

import requests
from fake_useragent import UserAgent


class PageScraper:
    def __init__(self, pages):
        self.pages = pages
        self.ua = UserAgent(platforms='pc')
        self.headers = {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Sec-Gpc": "1",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Accept-Encoding": "gzip, deflate, br",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Accept-Language": "en,en-US;q=0,5"
        }

    def run(self):
        for page in self.pages:
            response = requests.get(page.url, headers=self.headers)
            html = response.text
            time.sleep(0.3 + random.randrange(1, 10) / 10.0)
