import logging

from colorama import Fore, Style

logger = logging.getLogger("pythonLog")  # create logger named "pythonLog"
logger.root.setLevel(logging.INFO)

LOG_COLOR = {
    logging.DEBUG: Fore.WHITE,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.RED + Style.BRIGHT
}


class ColorFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, color=True):
        super().__init__(fmt, datefmt)
        self.color = color

    def format(self, record):
        message = super().format(record)
        if self.color:
            log_color = LOG_COLOR.get(record.levelno, Fore.WHITE)
            message = f"{log_color}{message}{Style.RESET_ALL}"
        return message


def setup_logger(color=True):
    logger.propagate = False

    if not logger.hasHandlers():
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        # formatter = ColorFormatter('%(asctime)s | %(levelname)s | %(message)s', datefmt="%H:%M:%S", color=color)
        # console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
