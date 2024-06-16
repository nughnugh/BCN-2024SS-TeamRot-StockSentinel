from Database import insert_stock, insert_news_source, DUMMY_SOURCE_STRING
from Source import Source
from Stock import Stock


def db_setup():
    insert_stock(Stock('Apple', 'AAPL',0))
    insert_news_source(Source(DUMMY_SOURCE_STRING, ' '))
    insert_news_source(Source('Forbes', 'www.forbes.com'))
