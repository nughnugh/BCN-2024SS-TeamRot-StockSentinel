import requests
from bs4 import BeautifulSoup
from Stock import Stock
from fake_useragent import UserAgent

class FinanceScraper:
    def __init__(self, stocks: list[Stock]):
        self.stocks = stocks
        headers = {"User-Agent": UserAgent(platforms='pc').random}
        self.client = requests.Session()
        self.client.headers.update(headers)

    def get_stock_price(self):
        for stock in self.stocks:
            url = f"https://finance.yahoo.com/quote/{stock.ticker_symbol}/history/"
            response = self.client.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find('tbody')
                rows = table.find_all('tr')
                todays_row = rows[0]
                cells = todays_row.find_all('td')
                price = cells[4].text
                if price:
                    try:
                        price = float(price)
                        stock.price = price
                    except ValueError:
                        continue
                else:
                    continue
            else:
                continue

        return self.stocks
