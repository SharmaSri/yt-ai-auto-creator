import logging
from logging import Formatter, FileHandler, StreamHandler
from config import OUTPUT_DIR
import os

LOG_FILE = os.path.join(OUTPUT_DIR, 'logs', 'run.log')
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)  # make sure log dir exists

def setup_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        # Stream handler
        sh = StreamHandler()
        sh.setFormatter(Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(sh)
        # File handler
        fh = FileHandler(LOG_FILE)
        fh.setFormatter(Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(fh)
    return logger


logger = setup_logger()