import logging
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from Stock import Stock
from fake_useragent import UserAgent
from Database import get_all_stocks

logger = logging.getLogger(__name__)

#alter FinanceScraper. Wurde von FinScraper ersetzt, hat auf einmal aus unbekannten Gründen nur noch mit VPN in den USA funktioniert
class FinanceScraper:
    def __init__(self):
        self.stocks = get_all_stocks()
        headers = {
<<<<<<< HEAD:sys-src/webscraper/FinanceScraper.py
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,/;q=0.8",
            "Referer": "http://www.google.com/"
=======
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',  # Do Not Track Request Header
            'Connection': 'close'
>>>>>>> webscraper:Junk/FinanceScraper.py
        }
        self.client = requests.Session()
        self.client.headers.update(headers)

    def get_stock_price(self, stock: Stock, min_max: tuple):
        price_data = []
        url = f"https://finance.yahoo.com/quote/{stock.ticker_symbol}/history/"
        response = self.client.get(url)
        #print(response.text)
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
                        if min_max is None:
                            min_max = (datetime(6666, 6, 7), datetime(2002, 7, 5))

                        if (date < min_max[0]) or (date > min_max[1]):  #nur neue Daten von Interesse
                            price = price.replace(',','')
                            price = float(price)
                            stock_tuple = (stock.db_id, date, price)
                            price_data.append(stock_tuple)

                    except ValueError:
                        logger.error(f"Could not parse price {price}")
        return price_data

    def get_all_prices(self, date_range: dict):
        price_data_super = []
        for stock in self.stocks:
            print(stock.ticker_symbol)
            min_max = date_range.get(stock.db_id)
            price_data_super.append(self.get_stock_price(stock, min_max))
        return price_data_super
