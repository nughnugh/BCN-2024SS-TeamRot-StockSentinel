from datetime import datetime

from DataImporter.common.DataModel.Source import Source
from DataImporter.common.DataModel.Stock import Stock

class PageData:
    def __init__(self, source: Source,
                 stock: Stock,
                 url: str,
                 title: str,
                 pub_date: datetime,
                 source_url: str,
                 ticker_related: bool,
                 timeout_cnt=0,
                 db_id=None):
        self.db_id = db_id
        self.source = source
        self.stock = stock
        self.url = url
        self.title = title
        self.pub_date = pub_date
        self.sentiment_exists = False,
        self.sentiment = [0.0,0.0,0.0,0.0]      #negativ, neutral, positiv, compound
        self.timeout_cnt = timeout_cnt
        self.source_url = source_url
        self.ticker_related = ticker_related

        self.content = ""
        self.headline = None
        self.description = None
        self.keywords = None
        self.sentences = []
        self.success = False
