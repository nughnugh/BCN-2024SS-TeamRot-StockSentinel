import unittest
from datetime import datetime as dt
from FinScraper import FinScraper
from Stock import Stock

class TestFinScraper(unittest.TestCase):
    def setUp(self):
        self.fin_scraper = FinScraper()
        self.stock1 = Stock('Apple','AAPL')
        self.stock2 = Stock('NVIDIA', 'NVDA')
        self.end_date = dt.strptime('02-14-2024', '%m-%d-%Y')
    def test_get_finance_data(self):
        result_df = self.fin_scraper.get_finance_data(self.stock1,start_date=None, end_date=self.end_date)
        expected_len = 30
        result_len = len(result_df)
        self.assertEqual(expected_len, result_len)


if __name__ == '__main__':
    unittest.main()
