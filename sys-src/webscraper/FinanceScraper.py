import requests
from bs4 import BeautifulSoup
from Stock import Stock
from fake_useragent import UserAgent

stock = Stock("Apple", "AAPL")
stocks = [stock]

class FinanceScraper:
    def __init__(self, stocks: list[Stock]):
        self.stocks = stocks
        headers = {"User-Agent": UserAgent(platforms='pc').random}
        self.client = requests.Session()
        self.client.headers.update(headers)

    def get_stock_price(self):
        for stock in self.stocks:
            url = f"https://finance.yahoo.com/quote/{stock.ticker_symbol}"
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                price_span = soup.find('fin-streamer', {'data-symbol': stock.ticker_symbol, 'data-field': 'regularMarketPrice'})

                if price_span:
                    price_txt = price_span.txt
                    return price_txt
                    try:
                        price = float(price_txt.replace(',', ''))
                        return price
                    except ValueError:
                        return "Fehler bei der Umwandlung des Preises"

                else:
                    return "Aktienpreis nicht gefunden"
            else:
                return "Fehler beim Abrufen der Seite"



finScraper = FinanceScraper(stocks)
print(finScraper.get_stock_price())