from GoogleCrawler import GoogleCrawler
from PageScraper import PageScraper
from Source import Source
from Stock import Stock

# test webcrawler
googleCrawler = GoogleCrawler(Stock('Apple'), Source('Forbes', 'www.forbes.com'))
pages = googleCrawler.run()
# pageScraper = PageScraper(pages)
# pageScraper.run()
