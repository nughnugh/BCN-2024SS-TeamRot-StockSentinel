from datetime import datetime
from Source import Source
from Stock import Stock

class PageData:
    def __init__(self, source: Source,
                 stock: Stock,
                 url: str,
                 title: str,
                 pub_date: datetime,
                 source_url: str,
                 ticker_related: bool,
                 timeout=False,
                 timeout_cnt=0,
                 db_id=None):
        self.db_id = db_id
        self.source = source
        self.stock = stock
        self.url = url
        self.title = title
        self.pub_date = pub_date
        self.content = ""
        self.sentiment_exists = False,
        self.sentiment = [0.0,0.0,0.0,0.0]      #negativ, neutral, positiv, compound
        self.timeout = timeout
        self.timeout_cnt = timeout_cnt
        self.source_url = source_url
        self.ticker_related = ticker_related
