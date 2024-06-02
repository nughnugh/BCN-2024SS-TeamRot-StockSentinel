import random
import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from PageData import PageData


class PageCrawler:
    def __init__(self, pages: list[PageData]):
        self.pages = pages
        headers = {"User-Agent": UserAgent(platforms='pc').random}
        self.client = requests.Session()
        self.client.headers.update(headers)

    def getContent(self):
        for page in self.pages:
            try:
                response = requests.get(page.url, timeout=(1,1))
                #print("basst")
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    page.content = soup.get_text()
                    time.sleep(0.3 + random.randrange(1, 10) / 10.0)
                else:
                    return f"Error fetching the page: {response.status_code}"
            except requests.exceptions.Timeout:
                print(f"Request to {page.url} timed out")
                page.timeout = True
            except requests.exceptions.RequestException as e:
                print(f"Undefined request error {e}")
                page.timeout = True
        return self.pages