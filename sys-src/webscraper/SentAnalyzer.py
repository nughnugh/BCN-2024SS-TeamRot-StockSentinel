import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from statistics import mean
from PageData import PageData

sia = SentimentIntensityAnalyzer()


async def analyze(page: PageData) -> PageData:
    if not page.timeout:
        text = page.content
        scores = [sia.polarity_scores(sentence) for sentence in nltk.sent_tokenize(text)]
        if not scores:
            print(f'Leere Liste, Inhalt:{page.content} url: {page.url}')
            return page
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
        page.sentiment_exists = True
    return page
