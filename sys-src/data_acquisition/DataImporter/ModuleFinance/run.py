from DataImporter.common.misc.db_setup import db_setup
from .FinanceDataProcess import FinanceDataProcess
from DataImporter.common.misc.LoggingHelper import init_logger

if __name__ == '__main__':
    init_logger('FinanceProcess')
    db_setup()
    fin_process = FinanceDataProcess()
    fin_process.run()

