import datetime

import psycopg2
import os
from dotenv import load_dotenv
import logging

from psycopg2.extras import execute_values

from FinanceScraper import FinanceScraper
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
        query = 'SELECT EXISTS (SELECT 1 FROM stock WHERE name = %s OR ticker_symbol = %s)'
        cursor.execute(query, (stock.name, stock.ticker_symbol, stock.price))
        if cursor.fetchone()[0]:
            logger.info(f'Stock already exists - {stock.name} {stock.ticker_symbol} {stock.price}')
        else:
            query = 'INSERT INTO stock (name, ticker_symbol,price) VALUES (%s, %s, %s) RETURNING stock_id'
            cursor.execute(query, (stock.name, stock.ticker_symbol, stock.price))
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
        query = 'SELECT EXISTS (SELECT 1 FROM news_source WHERE name = %s OR url = %s)'
        cursor.execute(query, (news_source.name, news_source.url))
        if cursor.fetchone()[0]:
            logger.info(f'News source already exists - {news_source.name} {news_source.url}')
        else:
            query = 'INSERT INTO news_source (name, url) VALUES (%s, %s) RETURNING news_source_id'
            cursor.execute(query, (news_source.name, news_source.url))
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
                           item.title))
    try:
        query = """
            INSERT INTO stock_news (stock_id, news_source_id, url, ticker_related, pub_date, title) VALUES %s
        """
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
        query = 'SELECT stock_id, name, ticker_symbol,price FROM stock'
        cursor.execute(query)
        stocks = cursor.fetchall()
        for stock in stocks:
            stock_list.append(Stock(db_id=stock[0], name=stock[1], ticker_symbol=stock[2], price=stock[3]))
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


def get_news_time_span(stock: Stock, source: Source, ticker_related: bool) -> (bool, datetime, datetime):
    cursor = conn.cursor()
    datetime_min: datetime = None
    datetime_max: datetime = None
    try:
        query = """
        SELECT min(pub_date), 
               max(pub_date) 
          FROM stock_news 
         WHERE stock_id = %s
           AND news_source_id = %s 
           AND ticker_related = %s
        """
        cursor.execute(query, (stock.db_id, source.db_id, ticker_related))
        data = cursor.fetchone()
        datetime_min = data[0]
        datetime_max = data[1]
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
    finally:
        cursor.close()
    return datetime_min, datetime_max


def get_unprocessed_news(limit_per_source) -> dict[int, list[PageData]]:
    cursor = conn.cursor()
    news_buckets: dict[int, list[PageData]] = {}
    try:
        query = f"""
        SELECT
          stock_news_id, url, title, timeout_cnt, news_source_id
        FROM (
          SELECT
            ROW_NUMBER() OVER (
                PARTITION BY news_source_id 
                ORDER BY news_source_id, timeout_cnt asc, stock_news_id desc
            ) AS rownum,
            t.*
          FROM
            stock_news t
          WHERE not sentiment_exists
        ) x
        WHERE
          x.rownum <= {limit_per_source}
        """
        cursor.execute(query)
        records = cursor.fetchall()
        for record in records:
            news_id = record[4]
            if news_id not in news_buckets:
                news_buckets[news_id] = []
            news_buckets[news_id].append(
                PageData(db_id=record[0], url=record[1], title=record[2], timeout_cnt=record[3],
                         source=None, stock=None, pub_date=None, ticker_related=None,
                         source_url=None))
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
    finally:
        cursor.close()
    return news_buckets


# TODO generalize update for all values..?
def update_news(news_list: list[PageData]):
    cursor = conn.cursor()
    query = """
        update stock_news s
        set
            sentiment_exists = t.sentiment_exists,
            sentiment = t.sentiment,
            timeout_cnt = t.timeout_cnt
        from (values %s) as t(stock_news_id, sentiment_exists, sentiment, timeout_cnt)
        where s.stock_news_id = t.stock_news_id;
    """
    rows_to_update = []
    for news in news_list:
        rows_to_update.append(
            (news.db_id, news.sentiment_exists, news.sentiment[3], news.timeout_cnt)
        )
    try:
        execute_values(cursor, query, rows_to_update)
        conn.commit()
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
        conn.rollback()
    finally:
        cursor.close()


def cleanup_timeout(max_retries: int):
    cursor = conn.cursor()
    try:
        query = 'DELETE FROM stock_news WHERE timeout_cnt >= %s'
        cursor.execute(query, (max_retries,))
        conn.commit()
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
        conn.rollback()
    finally:
        cursor.close()

get_dummy_source()
def insert_stock_value():
    stock_list = get_all_stocks()
    cursor = conn.cursor()
    try:
        FinScraper = FinanceScraper(stock_list)
        stock_list = FinScraper.get_stock_price()
        for stock in stock_list:
            query = 'UPDATE stock SET price = %? WHERE ticker_symbol = %?'
            cursor.execute(query, (stock.name, stock.ticker_symbol,stock.price))
        conn.commit()
        logger.info('Stock values updated successfully')

    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
        conn.rollback()
    finally:
        cursor.close()

"""
def get_all_tables():
    cursor = conn.cursor()
    try:
        query = ""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ""
        cursor.execute(query)
        tables = cursor.fetchall()
        for table in tables:
            print(table[0])
    except Exception as e:
        print('unexpected exception: ' + repr(e))
    finally:
        cursor.close()

get_all_tables()

def get_table_columns(table_name):
    cursor = conn.cursor()
    try:
        query = ""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = %s
        ""
        cursor.execute(query, (table_name,))
        columns = cursor.fetchall()
        for column in columns:
            print(f"Name: {column[0]}, Type: {column[1]}, Nullable: {column[2]}, Default: {column[3]}")
    except Exception as e:
        print('unexpected exception: ' + repr(e))
    finally:
        cursor.close()

get_table_columns('stock_price')  # Beispiel für die 'stock'-Tabelle
"""