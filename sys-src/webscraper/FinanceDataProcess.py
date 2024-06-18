from Database import insert_stock_price
from FinanceScraper import FinanceScraper

class FinanceDataProcess:
    def __init__(self):
        self.FinScraper = FinanceScraper()
        self.entire_price_data = self.FinScraper.get_all_prices()

    def push_data_to_db(self):
        insert_stock_price(self.entire_price_data)