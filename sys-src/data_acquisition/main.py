from DataImporter.ModuleFinance.FinanceDataProcess import FinanceDataProcess
from DataImporter.common.misc.LoggingHelper import init_logger

init_logger('main', False)

fin_process = FinanceDataProcess()
fin_process.run()

