from Source import Source
from Stock import Stock


class PageData:
    def __init__(self, source: Source, stock: Stock, url, title, pub_date):
        self.source = source
        self.stock = stock
        self.url = url
        self.title = title
        self.pub_date = pub_date
        self.content = ""
        self.sentiment = 0.0
        self.timeout = False
