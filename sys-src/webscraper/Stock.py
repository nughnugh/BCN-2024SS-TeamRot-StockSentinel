class Stock:
    def __init__(self, name: str, ticker_symbol: str, db_id=None):
        self.db_id = db_id
        self.name = name
        self.ticker_symbol = ticker_symbol