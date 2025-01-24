import logging,os
from .path_utils import mkdirs
from logging.handlers import RotatingFileHandler
from abstract_utilities import get_logFile
def get_logFile(bpName,maxBytes=100000, backupCount=3):
    # Configure logging
    log_dir = mkdirs('logs')
    log_path = os.path.join(log_dir,f'{bpName}.log')
    log_handler = RotatingFileHandler(log_path, maxBytes=100000, backupCount=backupCount)
    log_handler.setLevel(logging.INFO)
    logger = logging.getLogger(bpName)
    logger.addHandler(log_handler)
    logger.basicConfig(level=logger.INFO)
    return logger
