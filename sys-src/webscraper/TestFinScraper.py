import unittest
from datetime import datetime as dt, timedelta
from FinScraper import FinScraper
from Stock import Stock
import numpy as np

class TestFinScraper(unittest.TestCase):
    def setUp(self):
        self.fin_scraper = FinScraper()
        self.stock1 = Stock('Apple','AAPL')
        self.end_date = dt.strptime('02-14-2024', '%m-%d-%Y')

    def test_get_finance_data(self):
        result_df = self.fin_scraper.get_finance_data(self.stock1,start_date=None, end_date=self.end_date)
        expected_len = 30
        result_len = len(result_df)

        max_result_df = result_df.nlargest(3, ["Close"])
        max_result = max_result_df["Close"].to_numpy()
        expected_max_result = np.array([195.179993, 194.500000, 194.169998])  #Data checked manually from Yahoo Finance

        self.assertEqual(expected_len, result_len)
        self.assertTrue((expected_max_result == max_result).all())

    def test_get_all_data(self):
        date = dt.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=2)
        date_dict = {}
        stock_count = 0
        for stock in self.fin_scraper.stocks:
            date_dict[stock.db_id] = date
            stock_count += 1
        result_df = self.fin_scraper.get_all_data(date_dict)

        self.assertEqual(stock_count, len(result_df))


if __name__ == '__main__':
    unittest.main()
