from .FinanceDataProcess import FinanceDataProcess
from DataImporter.common.misc.LoggingHelper import init_logger

if __name__ == '__main__':
    init_logger('FinanceProcess')
    fin_process = FinanceDataProcess()
    fin_process.run()

