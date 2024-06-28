import binascii
from urllib.parse import urlparse

from DataImporter.common.DataModel.PageData import PageData
from DataImporter.common.DataModel.Source import Source
from DataImporter.common.DataModel.Stock import Stock
from fake_useragent import UserAgent
import datetime
import requests
import xml.etree.ElementTree as ET
import base64
import dateparser

import logging
logger = logging.getLogger(__name__)

COOKIES = {
    "CONSENT": "PENDING+987",
    "SOCS": "CAESHAgBEhJnd3NfMjAyMzA4MTAtMF9SQzIaAmRlIAEaBgiAo_CmBg"
}


class SearchTimeAggregate:
    HOUR = 'h'
    DAY = 'd'
    MONTH = 'm'


ddp = dateparser.date.DateDataParser()


class GoogleCrawler:
    def __init__(
            self, stock: Stock,
            existing_sources: dict,
            search_time_start: datetime.date,
            search_time_end: datetime.date,
            source: Source,
            search_by_ticker: bool = True,
            language: str = 'en',
            country: str = 'US',
    ):
        self.stock = stock
        self.source = source
        self.existing_sources = existing_sources
        self.search_time_start = search_time_start
        self.search_time_end = search_time_end
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
        search_str += f'site:{self.source.url}'
        search_str += f'+after:{self.search_time_start}+before:{self.search_time_end}+'
        # short tickers might give wrong results, search with name instead
        if self.search_by_ticker and len(self.stock.ticker_symbol) >= 3:
            search_str += f'intitle:{self.stock.ticker_symbol}'
        else:
            # replace special characters in name
            search_name = self.stock.name.translate({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`'~-=_+"})
            search_name = search_name.replace(' ', '%20')
            search_str += f'intitle:{search_name}'
        lan = f'hl={self.language}-{self.country}&gl={self.country}&ceid={self.country}:{self.language}'
        search_url = f'https://news.google.com/rss/{search_str}&{lan}'
        return search_url

    def parse_item(self, item) -> PageData | None:
        title = item.find('title').text
        pub_date = ddp.get_date_data(item.find('pubDate').text).date_obj
        source_url = urlparse(item.find('source').attrib['url']).netloc
        # links are encoded by google, use base64 decoder to avoid redirection
        encoded = item.find('guid').text
        try:
            decoded = base64.b64decode(encoded + '==')
        except binascii.Error as e:
            # decoded = base64.b64decode(encoded[-1] + '==')
            logger.error(repr(e))
            return None

        # url = 'https://' + str(base64.b64decode(encoded)[4: -3]).split('https://')[1]
        try:
            url = 'https://' + str(decoded[4: -3]).split('https://')[1]
        except IndexError as e:
            logger.error(f'{repr(e)} decoded={decoded}')
            return None
        # cleanup url
        url = url.replace('\'', '')
        url = url.split('\\')[0]

        source = self.source

        return PageData(source=source, stock=self.stock, url=url, title=title,
                        pub_date=pub_date, source_url=source_url, ticker_related=self.search_by_ticker)

    def run(self) -> list[PageData]:
        res = self.client.get(self.build_search_url())
        root = ET.fromstring(res.text)
        logger.info(self.build_search_url())
        channel = root.find('channel')
        pages = []
        if not channel:
            return pages
        for item in channel.findall('item'):
            page = self.parse_item(item)
            # linked pages may contain articles that were recently updated, but since the provided time is wrong
            # the data is unusable
            if page and self.search_time_start <= page.pub_date.date() <= self.search_time_end:
                pages.append(page)
        return pages
