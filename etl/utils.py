# utility functions for timestamp and logger
import logging
from datetime import datetime, timezone
import os


def setup_logger(log_file='logs/error.log'):
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    logger = logging.getLogger("ETLLogger")
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger

def get_utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()
