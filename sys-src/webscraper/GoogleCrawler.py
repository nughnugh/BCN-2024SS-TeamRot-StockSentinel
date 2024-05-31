from urllib.parse import urljoin, urlparse
import requests

from PageData import PageData
from Source import Source
from Stock import Stock
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def build_google_str(search_str, start=0, sort_by_date=True):
    search_url = 'https://www.google.de/search?'
    search_url += f'q={search_str}&tbm=nws'
    if sort_by_date:
        search_url += ',sbd:1'
    search_url += f'&start={start}'
    return search_url


class GoogleCrawler:
    def __init__(self, stock: Stock, source: Source):
        self.stock = stock
        self.source = source
        self.soup = None
        self.linked_pages = []
        self.linked_urls = set()
        self.url_docs = {}
        self.cookies = {
            "CONSENT": "PENDING+987",
            "SOCS": "CAESHAgBEhJnd3NfMjAyMzA4MTAtMF9SQzIaAmRlIAEaBgiAo_CmBg"
        }
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
        self.banned = False
        print(self.headers["User-Agent"])

    def get_linked_pages(self, url):
        for link in self.soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            parsed_url = urlparse(path)
            if 'google' not in str(parsed_url.netloc) and path is not None and path != '#':
                # time = link.findNext('div', {'class': 'OSrXXb rbYSKb LfVVr'})
                yield PageData(self.source, self.stock, path)

    def run(self):
        search_str = f'site:{self.source.url} {self.stock.name}'
        search_url = build_google_str(search_str)
        response = requests.get(search_url, headers=self.headers, cookies=self.cookies)
        html = response.text
        self.soup = BeautifulSoup(html, 'html.parser')
        pages = []
        for page in self.get_linked_pages(search_url):
            pages.append(page)
        return pages
