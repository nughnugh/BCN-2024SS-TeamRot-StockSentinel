from DataImporter.common.Database.Database import insert_stock_price, get_finance_time
from .FinScraper import FinScraper


class FinanceDataProcess:
    def __init__(self):
        self.fin_scraper = FinScraper()

    def run(self):
        all_dates = get_finance_time()
        entire_price_data = self.fin_scraper.get_all_data(all_dates)
        insert_stock_price(entire_price_data)
