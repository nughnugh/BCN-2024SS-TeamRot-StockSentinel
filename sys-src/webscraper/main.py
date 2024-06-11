from datetime import datetime
from GoogleCrawler import GoogleCrawler
from PageCrawler import PageCrawler
from PageData import PageData
from SentAnalyzer import SentAnalyzer
from Source import Source
from Stock import Stock
import nltk

nltk.download('vader_lexicon')
nltk.download('punkt')

# test webcrawler
stock = Stock('Apple', 'AAPL')
source = Source('Forbes', 'www.forbes.com')
# TODO
existing_sources = {}

date_str = '09-19-2022'
from_time = datetime.strptime(date_str, '%m-%d-%Y').date()

googleCrawler = GoogleCrawler(stock, existing_sources, 'd', 30, source=source, search_by_ticker=False)
#googleCrawler = GoogleCrawler(stock, existing_sources, 'd', 30)
pages = googleCrawler.run()

pageCrawler = PageCrawler(pages[:10])
pages = pageCrawler.getContent()

sentimentAnal = SentAnalyzer(pages)
sentimentAnal.analyze()

#for page in pages:
    #print(page.stock.name, page.source.name, page.pub_date, page.url)
# pageScraper = PageScraper(pages)
# pageScraper.run()
