import threading
from Database import insert_stock_price, get_finance_time
from FinanceScraper import FinanceScraper


class FinanceDataProcess(threading.Thread):
    def __init__(self):
        super().__init__()
        self.fin_scraper = FinanceScraper()

    def run(self):
        date_range = get_finance_time()
        entire_price_data = self.fin_scraper.get_all_prices(date_range)
        insert_stock_price(entire_price_data)
