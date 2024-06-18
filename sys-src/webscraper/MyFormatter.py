import logging

grey = "\x1b[38;20m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"

class MyFormatter(logging.Formatter):
    def __init__(self, is_console):
        normal_format = "%(asctime)s [%(levelname)-5.5s] [%(name)-12.12s]   %(message)s"
        error_format = "%(asctime)s [%(levelname)-5.5s] [%(filename)s:%(lineno)s - %(funcName)20s() ]  %(message)s"

        if is_console:
            self.FORMATS = {
                logging.DEBUG: grey + normal_format + reset,
                logging.INFO: grey + normal_format + reset,
                logging.WARNING: yellow + normal_format + reset,
                logging.ERROR: red + error_format + reset,
                logging.CRITICAL: bold_red + error_format + reset
            }
        else:
            self.FORMATS = {
                logging.DEBUG: normal_format,
                logging.INFO: normal_format,
                logging.WARNING: normal_format,
                logging.ERROR: error_format,
                logging.CRITICAL: error_format
            }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
