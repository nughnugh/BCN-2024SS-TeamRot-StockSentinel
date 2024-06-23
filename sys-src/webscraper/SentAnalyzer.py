import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from statistics import mean
from PageData import PageData

sia = SentimentIntensityAnalyzer()

def tokenize(page: PageData)-> list[str]:
    sentences = []
    for sentence in nltk.sent_tokenize(page.content):
        if sentence.count("\n") == 0:   #to prevent new-line "sentences"
            sentences.append(sentence.strip())
    return sentences

def analyze(page: PageData) -> PageData:
    scores = [sia.polarity_scores(sentence) for sentence in tokenize(page)]

    for k in range(5):    #headline and description are more important than average sentence
        scores.append(sia.polarity_scores(page.headline))
        scores.append(sia.polarity_scores(page.description))

    if not scores:
        print(f'Leere Liste, Inhalt:{page.content} url: {page.url}')
        page.timeout_cnt += 1
        return page
    neg_scores = [score['neg'] for score in scores]
    neu_scores = [score['neu'] for score in scores]
    pos_scores = [score['pos'] for score in scores]
    compound_scores = [score['compound'] for score in scores]

    page.sentiment = [
        mean(neg_scores),
        mean(neu_scores),
        mean(pos_scores),
        mean(compound_scores)*1.8
    ]
    page.sentiment_exists = True
    return page
