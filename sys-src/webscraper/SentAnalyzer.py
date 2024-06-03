import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from statistics import mean
from PageData import PageData

class SentAnalyzer:
    def __init__(self, pages: list[PageData]):
        self.pages = pages

    def analyze(self):
        sia = SentimentIntensityAnalyzer()
        for page in self.pages:
            if not page.timeout:
                text = page.content
                scores = [sia.polarity_scores(sentence)["compound"] for sentence in nltk.sent_tokenize(text)]
                if not scores:
                    print(f'Leere Liste, Inhalt:{page.content} url: {page.url}')
                    continue
                page.sentiment = mean(scores)
                print(page.sentiment)