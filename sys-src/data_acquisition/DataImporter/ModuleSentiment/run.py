from .SentimentProcess import SentimentProcess
from DataImporter.common.misc.LoggingHelper import init_logger

if __name__ == '__main__':
    init_logger('SentimentProcess')
    sentimentProcess = SentimentProcess(0.3, 1)
    sentimentProcess.run()
