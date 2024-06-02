from PageData import PageData
from Source import Source
from Stock import Stock
from fake_useragent import UserAgent
import datetime
import requests
from dateutil.relativedelta import relativedelta
import xml.etree.ElementTree as ET
import base64

COOKIES = {
    "CONSENT": "PENDING+987",
    "SOCS": "CAESHAgBEhJnd3NfMjAyMzA4MTAtMF9SQzIaAmRlIAEaBgiAo_CmBg"
}


class SearchTimeAggregate:
    HOUR = 'h'
    DAY = 'd'
    MONTH = 'm'


class GoogleCrawler:
    def __init__(
            self, stock: Stock,
            existing_sources: dict,
            search_time_agg: str,
            search_time_span: int,
            search_time_start: datetime.date = None,
            source: Source = None,
            search_by_ticker: bool = True,
            language: str = 'en',
            country: str = 'US',
    ):
        self.stock = stock
        self.source = source
        self.existing_sources = existing_sources
        self.search_time_agg = search_time_agg
        self.search_time_span = search_time_span
        self.search_time_start = search_time_start
        self.search_by_ticker = search_by_ticker

        headers = {
            "User-Agent": UserAgent(platforms='pc').random
        }

        self.client = requests.Session()
        self.client.headers.update(headers)
        self.client.headers.update(COOKIES)

        self.language = language.lower()
        self.country = country.upper()

    def build_search_url(self):
        search_str = 'search?q='
        if self.search_by_ticker:
            search_str += f'intitle:{self.stock.ticker_symbol}'
        else:
            search_str += self.stock.name

        if self.source:
            search_str += f'+site:{self.source.url}'
        if self.search_time_start:
            before = self.search_time_start
            after = (self.search_time_start -
                     relativedelta(
                         months=((self.search_time_agg == SearchTimeAggregate.MONTH) * self.search_time_span),
                         days=((self.search_time_agg == SearchTimeAggregate.DAY) * self.search_time_span),
                         hours=((self.search_time_agg == SearchTimeAggregate.HOUR) * self.search_time_span),
                     ))
            search_str += f'+after:{after}+before:{before}'
        else:
            search_str += f'+when:{self.search_time_span}{self.search_time_agg}'
        lan = f'hl={self.language}-{self.country}&gl={self.country}&ceid={self.country}:{self.language}'
        search_url = f'https://news.google.com/rss/{search_str}&{lan}'
        return search_url

    def parse_item(self, item) -> PageData:
        title = item.find('title').text
        pubDate = item.find('pubDate').text
        source_url = item.find('source').attrib['url']
        # links are encoded by google, use base64 decoder to avoid redirection
        encoded = item.find('guid').text + '=='
        url = 'https://' + str(base64.b64decode(encoded)[4: -3]).split('https://')[1]
        # cleanup url
        url = url.replace('\'', '')
        url = url.split('\\')[0]

        if self.source:
            return PageData(self.source, self.stock, url, title, pubDate)
        if source_url not in self.existing_sources:
            # TODO get source name
            self.existing_sources[source_url] = Source('UNKNOWN', source_url, False)
        return PageData(self.existing_sources.get(source_url), self.stock, url, title, pubDate)

    def run(self) -> list[PageData]:
        res = self.client.get(self.build_search_url())
        root = ET.fromstring(res.text)
        print(self.build_search_url())
        channel = root.find('channel')
        pages = []
        if not channel:
            return pages
        for item in channel.findall('item'):
            pages.append(self.parse_item(item))
        return pages
