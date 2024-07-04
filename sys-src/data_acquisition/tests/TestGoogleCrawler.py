import unittest
from datetime import datetime

from DataImporter.common.DataModel.Source import Source
from DataImporter.common.DataModel.Stock import Stock
from DataImporter.ModuleNews.GoogleCrawler import GoogleCrawler


class TestGoogleCrawler(unittest.TestCase):
    def test_page_return(self):
        stock = Stock("Eli Lilly & Co", "LLY")
        source = Source("Forbes", "www.forbes.com")
        existing_sources = {}
        google_crawler = GoogleCrawler(stock=stock, existing_sources=existing_sources,
                                       search_time_start=datetime.strptime('01-01-2024', '%m-%d-%Y').date(),
                                       search_time_end=datetime.strptime('06-06-2024', '%m-%d-%Y').date(),
                                       source=source, search_by_ticker=False)
        pages = google_crawler.run()
        self.assertTrue(len(pages) > 10)


if __name__ == '__main__':
    unittest.main()