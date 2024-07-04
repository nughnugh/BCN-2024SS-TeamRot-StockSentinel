from DataImporter.ModuleSentiment.SentAnalyzer import analyze, tokenize
from DataImporter.common.Database.Database import get_all_stock_news, unlock_stock_news

stock_news_list = get_all_stock_news()
for news in stock_news_list:
    news.sentences = tokenize(news.content)
    analyze(news)
print('finished analysing')
unlock_stock_news(stock_news_list)
print('updated')
