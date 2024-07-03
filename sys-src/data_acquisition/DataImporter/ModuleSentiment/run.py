import signal

from DataImporter.common.Database.Database import unlock_old_stock_news
from .SentimentProcess import SentimentProcess
from DataImporter.common.misc.LoggingHelper import init_logger

if __name__ == '__main__':
    init_logger('SentimentProcess')
    unlock_old_stock_news()
    sentiment_process = SentimentProcess(1, 2)
    signal.signal(signal.SIGINT, sentiment_process.stop)
    signal.signal(signal.SIGTERM, sentiment_process.stop)
    sentiment_process.run()
