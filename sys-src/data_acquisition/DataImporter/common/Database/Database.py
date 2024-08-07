import datetime
import psycopg2
import os
from dotenv import load_dotenv
import logging
from psycopg2.extras import execute_values
from DataImporter.common.DataModel.PageData import PageData
from DataImporter.common.DataModel.Source import Source
from DataImporter.common.DataModel.Stock import Stock
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

load_dotenv(dotenv_path='../.env')
load_dotenv(dotenv_path='../../.env')

conn = psycopg2.connect(database=os.getenv("POSTGRES_DB"),
                        host=os.getenv("PG_HOST"),
                        user=os.getenv("POSTGRES_USER"),
                        password=os.getenv("POSTGRES_PASSWORD"),
                        port=os.getenv("PG_PORT")
                        )

DUMMY_SOURCE_STRING = 'ANY_SOURCE'


def insert_stock(stock: Stock) -> Stock:
    cursor = conn.cursor()
    try:
        query = 'SELECT EXISTS (SELECT 1 FROM stock WHERE name = %s OR ticker_symbol = %s)'
        cursor.execute(query, (stock.name, stock.ticker_symbol))
        if cursor.fetchone()[0]:
            logger.info(f'Stock already exists - {stock.name} {stock.ticker_symbol}')
        else:
            query = 'INSERT INTO stock (name, ticker_symbol) VALUES (%s, %s) RETURNING stock_id'
            cursor.execute(query, (stock.name, stock.ticker_symbol))
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
        collection.append((item.stock.db_id, item.source.db_id, item.url, item.source_url, item.ticker_related,
                           item.pub_date, item.title))
    try:
        query = """
            INSERT INTO stock_news (stock_id, news_source_id, url, source_url, ticker_related, pub_date, title) VALUES %s
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
    datetime_min = None
    datetime_max = None
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


def get_unprocessed_news(limit_per_source, sentiment_exists=False) -> dict[str, list[PageData]]:
    cursor = conn.cursor()
    news_buckets: dict[str, list[PageData]] = {}
    try:
        query = f"""
            UPDATE stock_news
               SET locked = true,
                   mod_date = now()
            WHERE stock_news.stock_news_id in (
                SELECT stock_news_id
                  FROM (
                      SELECT ROW_NUMBER() OVER (
                          PARTITION BY source_url
                          ORDER BY source_url, timeout_cnt asc, pub_date desc
                          ) AS rownum,
                                   t.*
                            FROM stock_news t
                            WHERE sentiment_exists = %(sentiment_exists)s
                              AND not locked
                  ) x
                  WHERE x.rownum <= %(limit_per_source)s
            )
            RETURNING stock_news_id, url, title, timeout_cnt, source_url
        """
        cursor.execute(query, {'limit_per_source': limit_per_source, 'sentiment_exists': sentiment_exists})
        records = cursor.fetchall()
        for record in records:
            source_url = record[4]
            if source_url not in news_buckets:
                news_buckets[source_url] = []
            news_buckets[source_url].append(
                PageData(db_id=record[0], url=record[1], title=record[2], timeout_cnt=record[3],
                         source_url=source_url, source=None, stock=None, pub_date=None,
                         ticker_related=None))
        conn.commit()
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
        conn.rollback()
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
            description = t.description,
            timeout_cnt = t.timeout_cnt,
            content     = t.content,
            locked = false,
            mod_date = now()
        from (values %s) as t(stock_news_id, sentiment_exists, sentiment, timeout_cnt, description, content)
        where s.stock_news_id = t.stock_news_id;
    """
    rows_to_update = []
    for news in news_list:
        rows_to_update.append(
            (news.db_id, news.sentiment_exists, news.sentiment[3], news.timeout_cnt, news.description, news.content)
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


def unlock_stock_news(news_list: list[PageData]):
    cursor = conn.cursor()
    query = """
        update stock_news s
           set locked = false
          from (values %s) as t(stock_news_id)
         where s.stock_news_id = t.stock_news_id;
    """
    rows_to_update = []
    for news in news_list:
        rows_to_update.append(
            (news.db_id,)
        )
    try:
        execute_values(cursor, query, rows_to_update)
        conn.commit()
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
        conn.rollback()
    finally:
        cursor.close()


def unlock_old_stock_news():
    cursor = conn.cursor()
    query = """
       update stock_news
          set locked = false
        where locked
          and mod_date is not null
          and EXTRACT(EPOCH FROM now() -  mod_date) > 60;
    """
    try:
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
        conn.rollback()
    finally:
        cursor.close()


def get_all_stock_news() -> list[PageData]:
    cursor = conn.cursor()
    news_list: list[PageData] = []
    try:
        query = f"""
            SELECT stock_news_id, url, title, timeout_cnt, source_url, content, description
              FROM STOCK_NEWS
             WHERE sentiment_exists
        """
        cursor.execute(query)
        records = cursor.fetchall()
        for record in records:
            page_data = PageData(db_id=record[0], url=record[1], title=record[2], timeout_cnt=record[3],
                                 source_url=record[4], source=None, stock=None, pub_date=None,
                                 ticker_related=None)
            page_data.content = record[5]
            page_data.description = record[6]
            news_list.append(page_data)
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
    finally:
        cursor.close()
    return news_list


def insert_stock_price(entire_price_data):
    data_list = []
    cursor = conn.cursor()
    try:
        for index, row in entire_price_data.iterrows():
            data_tuple = (row['stock_id'], row['stock_price_time'], row['stock_price_val'])
            data_list.append(data_tuple)
        try:
            query = """
                    INSERT INTO stock_price (stock_id, stock_price_time, stock_price_val) VALUES %s
                """
            execute_values(cursor, query, data_list)
            logger.info(f'inserted {len(data_list)} rows in stock_price')
            conn.commit()
        except Exception as e:
            logger.error('unexpected exception: ' + repr(e))
            conn.rollback()
    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
        conn.rollback()
    finally:
        cursor.close()


def get_finance_time() -> dict:
    cursor = conn.cursor()
    date_dic = defaultdict(list)
    max_date_dic = {}
    try:
        query = 'SELECT stock_price_time, stock_id FROM stock_price'
        cursor.execute(query)
        dates = cursor.fetchall()

        for date in dates:
            date_time, stock_id = date
            date_obj = date_time.strftime("%Y-%m-%d %H:%M:%S%z")
            date_dic[stock_id].append(date_obj)

        for stock_id, date_list in date_dic.items():
            max_date = max(date_list)

            max_date = max_date[:-14]

            max_date = datetime.strptime(max_date, '%Y-%m-%d')

            max_date_dic[stock_id] = max_date

    except Exception as e:
        logger.error('unexpected exception: ' + repr(e))
    finally:
        cursor.close()
    return max_date_dic
