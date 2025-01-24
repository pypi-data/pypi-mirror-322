import logging
import os
from .path_utils import mkdirs
from logging.handlers import RotatingFileHandler
# from abstract_utilities import get_logFile  # Potential conflict - consider removing or renaming

def get_logFile(bpName, maxBytes=100000, backupCount=3):
    """Return a logger that writes messages at INFO level or above to a rotating file."""
    # Create logs directory if it doesn't exist
    log_dir = mkdirs('logs')
    log_path = os.path.join(log_dir, f'{bpName}.log')

    # Create or get the named logger
    logger = logging.getLogger(bpName)
    # Set the logger’s overall threshold to INFO (so DEBUG is suppressed)
    logger.setLevel(logging.INFO)

    # Configure the rotating file handler
    log_handler = RotatingFileHandler(log_path, maxBytes=maxBytes, backupCount=backupCount)
    # Set the file handler’s threshold to INFO as well
    log_handler.setLevel(logging.INFO)

    # Add the handler to the logger
    logger.addHandler(log_handler)

    return logger
