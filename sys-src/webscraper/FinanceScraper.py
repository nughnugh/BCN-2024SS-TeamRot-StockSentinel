import requests
from bs4 import BeautifulSoup
from Stock import Stock
from fake_useragent import UserAgent

stock1 = Stock("Apple", "AAPL",0)
stock2 = Stock("NVIDIA","NVDA",0)
stockss = [stock1,stock2]

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
                
                #price_span = soup.find('fin-streamer', class_='livePrice svelte-mgkamr', attrs={'data-symbol': stock.ticker_symbol})
                #table = soup.find('table', class_='table svelte-ewueuo')
                table = soup.find('tbody')
                rows = table.find_all('tr')
                todays_row = rows[0]
                cells = todays_row.find_all('td')
                price = cells[4].text
                if price:
                    try:
                        price = float(price)
                        stock.value = price
                    except ValueError:
                        continue
                else:
                    continue
            else:
                continue


finScraper = FinanceScraper(stockss)
finScraper.get_stock_price()
print(stock1.value)
print(stock2.value)