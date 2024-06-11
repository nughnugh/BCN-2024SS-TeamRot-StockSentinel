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
                scores = [sia.polarity_scores(sentence) for sentence in nltk.sent_tokenize(text)]
                if not scores:
                    print(f'Leere Liste, Inhalt:{page.content} url: {page.url}')
                    continue

                neg_scores = [score['neg'] for score in scores]
                neu_scores = [score['neu'] for score in scores]
                pos_scores = [score['pos'] for score in scores]
                compound_scores = [score['compound'] for score in scores]

                page.sentiment = [
                    mean(neg_scores),
                    mean(neu_scores),
                    mean(pos_scores),
                    mean(compound_scores)
                ]

                print(page.sentiment)
