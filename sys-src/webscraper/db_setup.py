from Database import insert_stock, insert_news_source, DUMMY_SOURCE_STRING
from Source import Source
from Stock import Stock


def db_setup():
    insert_stock(Stock('Apple', 'AAPL'))
    insert_stock(Stock('Nvidia', 'NVDA'))
    insert_stock(Stock('AMD', 'AMD'))
    insert_stock(Stock('Amazon', 'AMZN'))

    insert_news_source(Source(DUMMY_SOURCE_STRING, ' '))
    insert_news_source(Source('Forbes', 'www.forbes.com'))
    insert_news_source(Source('Nasdaq', 'www.nasdaq.com'))
    insert_news_source(Source('Yahoo Finance', 'finance.yahoo.com'))
    insert_news_source(Source('Investor Place', 'investorplace.com'))
    # insert_news_source(Source('Seeking Alpha', 'seekingalpha.com'))
