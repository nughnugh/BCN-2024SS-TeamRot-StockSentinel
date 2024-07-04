import unittest
from datetime import datetime as dt

from DataImporter.ModuleSentiment.PageScraper import PageScraper
from DataImporter.common.DataModel.PageData import PageData
from DataImporter.common.DataModel.Source import Source
from DataImporter.common.DataModel.Stock import Stock


class MyTestCase(unittest.TestCase):
    def setUp(self):
        source = Source('Wikipedia', 'https://de.wikipedia.org/')
        stock = Stock('Dummy','dum')
        self.page1 = PageData(source, stock, 'https://www.heise.de/news/APT-Angriff-auf-Fernwartungssoftware-Sicherheitsvorfall-bei-TeamViewer-9781567.html', 'heise.de', dt.strptime('07-05-2002', '%m-%d-%Y'), source.url, True)
        self.page_list = [self.page1]
        self.pageScraper = PageScraper(self.page_list, 'url', 5, 10)

    def test_process_page(self):
        success = self.pageScraper.process_page(self.page1)

        expected_headline = "APT-Angriff auf Fernwartungssoftware? Sicherheitsvorfall bei TeamViewer"
        expected_keywords = "APT, Cozy Bear, Cyberangriff, Fancy Bear, Fernwartungssoftware, Security, Teamviewer"
        expected_description = "Noch ist über das Ausmaß des Angriffs gegen die Fernwartungssoftware nicht viel bekannt - erste Hinweise auf die Urheber deuten auf Profis hin."

        self.assertEqual(expected_headline, self.page1.headline)
        self.assertEqual(expected_keywords, self.page1.keywords)
        self.assertEqual(expected_description, self.page1.description)
        self.assertTrue(success)
        self.assertTrue(self.page1.content is not None)


if __name__ == '__main__':
    unittest.main()
