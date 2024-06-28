import pandas as pd
from datetime import datetime as dt, timedelta
import calendar
import io
import requests
from Stock import Stock
from Database import get_all_stocks


class FinScraper:
    def __init__(self):
        self.stocks = get_all_stocks()
        self.base_url = 'https://query1.finance.yahoo.com/v7/finance/download/'
        self.headers = {
            'Accept': 'text/csv;charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
        }

    def get_finance_data(self, stock: Stock, start_date, end_date=None):
        if not end_date:
            end_date = dt.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if start_date is None:
            start_date = dt.strptime('01-01-2024', '%m-%d-%Y')
        else:
            start_date = start_date + timedelta(days=1)

        if start_date >= end_date:
            return pd.DataFrame()

        from_date = calendar.timegm(start_date.utctimetuple())

        to_date = calendar.timegm(end_date.utctimetuple())

        params = {
            'period1': str(from_date),
            'period2': str(to_date),
            'interval': '1d',
            'events': 'history',
            'includeAdjustedClose': 'true'
        }

        response = requests.request("GET", self.base_url + stock.ticker_symbol, headers=self.headers,
                                    params=params)
        if response.status_code < 200 or response.status_code > 299:
            print(response.status_code)
            print(stock.name, stock.ticker_symbol)
            return None
        else:
            csv = io.StringIO(response.text)
            df_unfiltered = pd.read_csv(csv)
            df_filtered = df_unfiltered[['Date', 'Close']].copy()
            df_filtered['stock_id'] = stock.db_id
            return df_filtered

    def get_all_data(self, all_dates:dict):
        big_df = pd.DataFrame()
        for stock in self.stocks:
            start_date = all_dates.get(stock.db_id)
            big_df = pd.concat([big_df, self.get_finance_data(stock, start_date)], ignore_index=True)
        big_df = big_df.rename(columns={'Date': 'stock_price_time', 'Close': 'stock_price_val'})
        return big_df

