from Source import Source
from Stock import Stock


class PageData:
    def __init__(self, source: Source, stock: Stock, url):
        self.source = source
        self.stock = stock
        self.url = url
        self.content = ""
