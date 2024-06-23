import logging
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from Stock import Stock
from fake_useragent import UserAgent
from Database import get_all_stocks
from Database import get_finance_time

logger = logging.getLogger(__name__)

price_data = []
price_data_super = []


class FinanceScraper:
    def __init__(self):
        self.stocks = get_all_stocks()
        headers = {"User-Agent": UserAgent(platforms='pc').random}
        self.client = requests.Session()
        self.client.headers.update(headers)
        self.date_range = get_finance_time()

    def get_stock_price(self, stock: Stock, date_range: dict):
        url = f"https://finance.yahoo.com/quote/{stock.ticker_symbol}/history/"
        response = self.client.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('tbody')
            rows = table.find_all('tr')

            for row in rows:
                cells = row.find_all('td')
                if len(cells) > 2:      #Dividendenzeilen sollen übersprungen werden
                    price = cells[4].text
                else:
                    continue
                date = cells[0].text

                if price and date:
                    try:
                        date = datetime.strptime(date, "%b %d, %Y")

                        min_max = date_range.get(stock.db_id)

                        if date < min_max[0] or date > min_max[1]:
                            price = float(price)
                            stock_tuple = (stock.db_id, date, price)
                            price_data.append(stock_tuple)

                    except ValueError:
                        logger.error(f"Could not parse price {price}")
        return price_data

    def get_all_prices(self):
        for stock in self.stocks:
            price_data_super.append(self.get_stock_price(stock, self.date_range))
            return price_data_super
