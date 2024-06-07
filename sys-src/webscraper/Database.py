import datetime

import psycopg2
import os
from dotenv import load_dotenv
import logging

from psycopg2.extras import execute_values

from PageData import PageData
from Source import Source
from Stock import Stock

logger = logging.getLogger(__name__)

load_dotenv(dotenv_path='../.env')
load_dotenv(dotenv_path='../postgres.env')

conn = psycopg2.connect(database=os.getenv("POSTGRES_DB"),
                        host=os.getenv("PG_HOST"),
                        user=os.getenv("POSTGRES_USER"),
                        password=os.getenv("POSTGRES_PASSWORD"),
                        port=os.getenv("PG_PORT")
                        )

DUMMY_SOURCE: Source
DUMMY_SOURCE_STRING = 'ANY_SOURCE'


def insert_stock(stock: Stock) -> Stock:
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO stock (name, ticker_symbol) VALUES (%s, %s) RETURNING stock_id',
                       (stock.name, stock.ticker_symbol))
        stock_id = cursor.fetchone()[0]
        stock.db_id = stock_id
        conn.commit()
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
        conn.rollback()
    finally:
        cursor.close()

    return stock


def insert_news_source(news_source: Source):
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO news_source (name, url) VALUES (%s, %s) RETURNING news_source_id',
                       (news_source.name, news_source.url))
        news_source_id = cursor.fetchone()[0]
        news_source.db_id = news_source_id
        conn.commit()
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
        conn.rollback()
    finally:
        cursor.close()

    return news_source


def remove_existing_news(stock_news: list[PageData]) -> list[PageData]:
    cursor = conn.cursor()
    collection = []
    stock_news_dict = {}
    for item in stock_news:
        collection.append(item.url)
        stock_news_dict[item.url] = item
    try:
        query = 'SELECT url FROM stock_news WHERE url = ANY (%s)'
        cursor.execute(query, (collection,))
        exclude_urls = cursor.fetchall()
        for url in exclude_urls:
            stock_news_dict.pop(url[0])

    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
    finally:
        cursor.close()

    return list(stock_news_dict.values())


def insert_stock_news_batch(stock_news: list[PageData]) -> list[PageData]:
    cursor = conn.cursor()
    collection = []
    for item in stock_news:
        collection.append((item.stock.db_id, item.source.db_id, item.url, item.ticker_related, item.pub_date,
                           item.timeout, item.title))
    try:
        query = 'INSERT INTO stock_news (stock_id, news_source_id, url, ticker_related, pub_date, timeout, title) VALUES %s'
        execute_values(cursor, query, collection)
        logger.info(f'inserted {len(stock_news)} stock news')
        conn.commit()
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
        conn.rollback()
    finally:
        cursor.close()

    return stock_news


def get_all_stocks() -> list[Stock]:
    cursor = conn.cursor()
    stock_list: list[Stock] = []
    try:
        query = 'SELECT stock_id, name, ticker_symbol FROM stock'
        cursor.execute(query)
        stocks = cursor.fetchall()
        for stock in stocks:
            stock_list.append(Stock(db_id=stock[0], name=stock[1], ticker_symbol=stock[2]))
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
    finally:
        cursor.close()
    return stock_list


def get_dummy_source():
    cursor = conn.cursor()
    global DUMMY_SOURCE
    try:
        query = 'SELECT news_source_id, name, url FROM news_source WHERE name = %s'
        cursor.execute(query, [DUMMY_SOURCE_STRING])
        data = cursor.fetchone()
        DUMMY_SOURCE = Source(db_id=data[0], name=data[1], url=data[2])
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
    finally:
        cursor.close()


def get_all_news_sources() -> list[Source]:
    cursor = conn.cursor()
    source_list: list[Source] = []
    try:
        query = 'SELECT news_source_id, name, url FROM news_source WHERE name <> %s'
        cursor.execute(query, [DUMMY_SOURCE_STRING])
        sources = cursor.fetchall()
        for source in sources:
            source_list.append(Source(db_id=source[0], name=source[1], url=source[2]))
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
    finally:
        cursor.close()
    return source_list


def get_news_time_span(stock: Stock, source: Source) -> (bool, datetime, datetime):
    cursor = conn.cursor()
    datetime_min: datetime = None
    datetime_max: datetime = None
    try:
        query = 'SELECT min(pub_date), max(pub_date) FROM stock_news WHERE stock_id = %s AND news_source_id = %s'
        cursor.execute(query, (stock.db_id, source.db_id))
        data = cursor.fetchone()
        datetime_min = data[0]
        datetime_max = data[1]
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
    finally:
        cursor.close()
    return datetime_min, datetime_max


get_all_news_sources()

