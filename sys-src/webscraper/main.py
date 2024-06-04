from datetime import datetime

from NewsCrawler import NewsCrawler, QueryMode

news_crawler = NewsCrawler(QueryMode.RECENT, datetime.strptime('01-01-2024', '%m-%d-%Y').date(), 7)
news_crawler.run()

#for page in pages:
    #print(page.stock.name, page.source.name, page.pub_date, page.url)
# pageScraper = PageScraper(pages)
# pageScraper.run()
