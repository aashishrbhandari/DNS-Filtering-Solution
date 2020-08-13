import logging
import time
from functools import wraps
from os import path, rename as file_rename
from datetime import datetime

from logging.handlers import RotatingFileHandler

from config.DnsServerStaticData import DnsServerStaticData

def timed(func):
    """ This decorator prints the execution time for the decorated function. """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        actual_func = func(*args, **kwargs)
        end_time = time.time()
        process_time_in_millis = (end_time - start_time) * 1000;
        logger.debug(f"{func.__name__} took [Raw: {process_time_in_millis} millis] [Round: {round(process_time_in_millis, 3)} millis]")
        #print(f"{func.__name__} took [Raw: {process_time_in_millis} millis] [Round: {round(process_time_in_millis, 3)} millis]")
        return actual_func

    return wrapper

def init_log():
    log_file = DnsServerStaticData.DNS_SERVER_LOG_FILE_FULL_PATH
    _logger = logging.getLogger("DnsFilterV1")

    # Rotate File on Application Restart [Implement Zipping it Later]
    if path.exists(log_file):
        curr_time_stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_rename(log_file, f"{log_file[:-4]}_{curr_time_stamp}.log")

    FORMAT = "[%(asctime)s] [%(threadName)s]: %(levelname)s %(message)s"

    logging.basicConfig(
        handlers = [RotatingFileHandler(log_file, maxBytes=200000000, backupCount=100,)],
        level = logging.DEBUG,
        format = FORMAT
    )
    return _logger


# main Logger
logger = init_log()

