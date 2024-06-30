from Database import insert_stock_price, get_finance_time
from FinanceScraper import FinanceScraper

class FinanceDataProcess:
    def __init__(self):
        self.FinScraper = FinanceScraper()
        self.date_range = get_finance_time()
        self.entire_price_data = self.FinScraper.get_all_prices(self.date_range)

    def push_data_to_db(self):
        insert_stock_price(self.entire_price_data)