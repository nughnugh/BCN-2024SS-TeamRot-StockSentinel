import requests
from bs4 import BeautifulSoup
from PageData import PageData


class PageCrawler:
    def __init__(self, pages: list[PageData]):
        self.pages = pages

    def getContent(self):

        for page in self.pages:
            response = requests.get(page.url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                page.content = soup.get_text()
                return page
            else:
                return f"Error fetching the page: {response.status_code}"
