from GoogleCrawler import GoogleCrawler
from Source import Source
from Stock import Stock

# test webcrawler
googleCrawler = GoogleCrawler(Stock('Apple'), Source('Forbes', 'www.forbes.com'))
googleCrawler.run()
