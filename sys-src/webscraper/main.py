from datetime import datetime

from Database import get_all_stocks, get_all_news_sources, insert_stock_news_batch
from GoogleCrawler import GoogleCrawler
from PageCrawler import PageCrawler
from Source import Source
from Stock import Stock


# test webcrawler
stock_list = get_all_stocks()
source_list = get_all_news_sources()

existing_sources = {}
for source in source_list:
    existing_sources[source.url] = source

date_str = '09-19-2022'
from_time = datetime.strptime(date_str, '%m-%d-%Y').date()

for stock in stock_list:
    for source in source_list:
        googleCrawler = GoogleCrawler(stock, existing_sources, 'd', 30, source=source, search_by_ticker=False)
        stock_news = googleCrawler.run()
        insert_stock_news_batch(stock_news)
    # googleCrawler = GoogleCrawler(stock, existing_sources, 'd', 7, search_by_ticker=True)
    # insert_stock_news_batch(stock_news)


#for page in pages:
    #print(page.stock.name, page.source.name, page.pub_date, page.url)
# pageScraper = PageScraper(pages)
# pageScraper.run()
