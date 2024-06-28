import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock
from statistics import mean
from PageData import PageData
import SentAnalyzer

class TestSentimentAnalysis(unittest.TestCase):

    def test_analyze(self):
        bad_page = PageData(source='Forbes', stock='Apple', url='oth-aw.de', title='testPage',pub_date=datetime(2002, 7, 5), source_url='oth-aw.de', ticker_related=True)
        bad_page.content = 'This is a very negative and bad review. Apple is soon filing bankruptcy. Apple employees are getting fired. Everyting is very bad'
        bad_page.headline = 'Apple soon to file bankruptcy'
        bad_page.description = 'Apple has lost all their money and is about to file bankruptcy according to new intel'

        bad_page = SentAnalyzer.analyze(bad_page)

        good_page = PageData(source='Forbes', stock='Nvidia', url='oth-aw.de', title='testPage',
                            pub_date=datetime(2002, 7, 5), source_url='oth-aw.de', ticker_related=True)
        good_page.content = 'This is a very positive and good review. Nvidias stock is skyrocketing. They are the richest hardware manufacturer. Everyting is super great'
        good_page.headline = 'Nvidia is rich and great'
        good_page.description = 'Nvidia has made a big profit'

        good_page = SentAnalyzer.analyze(good_page)

        self.assertTrue(bad_page.sentiment_exists)
        self.assertTrue(bad_page.sentiment[3] < -0.5)

        self.assertTrue(good_page.sentiment_exists)
        self.assertTrue(good_page.sentiment[3] > 0.5)

    def test_tokenize(self):
        page = PageData(source='Forbes',stock='Apple',url='oth-aw.de',title='testPage',pub_date=datetime(2002,7,5),source_url='oth-aw.de',ticker_related=True)
        page.content = 'This is a sentence. Another sentence. \n. Tokenize should split this string into tokens.'
        expected_result = ['This is a sentence.','Another sentence.','Tokenize should split this string into tokens.']

        result = SentAnalyzer.tokenize(page)

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()