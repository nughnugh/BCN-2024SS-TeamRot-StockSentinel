from DataImporter.ModuleSentiment.PageScraper import PageScraper
from DataImporter.ModuleSentiment.SentAnalyzer import analyze, tokenize
from DataImporter.common.DataModel.PageData import PageData
from DataImporter.common.misc.LoggingHelper import init_logger

init_logger('test')

def test():
    pageCrawler = PageScraper(None, None, 0.5, 1)
    urls = [
        #"https://investorplace.com/2024/01/aapl-amzn-msft-how-to-play-the-tech-giants-ahead-of-earnings/",
        #"https://finance.yahoo.com/news/heres-why-think-nvidia-nasdaq-110134610.html",

        #"https://www.forbes.com/sites/roberthart/2024/06/19/chip-stock-rally-continues-wednesday-after-ai-boom-catapults-nvidia-to-worlds-most-valuable-company/",
        #"https://www.nasdaq.com/articles/apple-aapl-the-critics-have-been-wrong-until-now-and-still-are",
        #"https://seekingalpha.com/article/4698469-apples-golden-moment"
        #"https://www.forbes.com/sites/dereksaul/2024/02/12/nvidia-is-now-more-valuable-than-amazon-and-google/"
        "https://in.investing.com/news/apple-could-generate-4-billion-in-revenue-from-vision-pro-sales-by-2027--morgan-stanley-432SI-3990232"
    ]
    for url in urls:
        print(url)
        page = PageData(source=None, stock=None, url=url, title=None, pub_date=None, source_url=None, ticker_related=False)
        pageCrawler.process_page(page)
        print("headline:", page.headline)
        print("description:", page.description)
        print("keywords:", page.keywords)
        # analyze(page)
        sentences = tokenize(page.content)
        content = '\n'.join(sentences)
        print("keywords:", content)
        print(page.sentiment[3])

test()