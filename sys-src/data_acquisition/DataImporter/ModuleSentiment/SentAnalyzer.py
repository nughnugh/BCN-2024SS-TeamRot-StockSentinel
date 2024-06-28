import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from statistics import mean
from DataImporter.common.DataModel.PageData import PageData

nltk.download('vader_lexicon')
nltk.download('punkt')
sia = SentimentIntensityAnalyzer()

def tokenize(page: PageData)-> list[str]:
    sentences = []
    for sentence in nltk.sent_tokenize(page.content):
        if sentence.count("\n") == 0:   #to prevent new-line "sentences"
            sentences.append(sentence.strip())
    return sentences

def analyze(page: PageData) -> PageData:
    sentences = tokenize(page)
    scores = [sia.polarity_scores(sentence) for sentence in sentences]

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
        (mean(compound_scores)-0.2)*1.5
    ]
    page.sentiment_exists = True
    page.content = "\n".join(sentences)
    return page
