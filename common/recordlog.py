import logging
import time
from logging.handlers import RotatingFileHandler
import os
from conf import setting

log_path = setting.FILE_PATH["LOG"]
log_path.mkdir(parents=True, exist_ok=True)
logfile_name = log_path / r"\test.{}.logs".format(time.strftime("%Y%m%d"))


def get_log():
    """
        获取日志记录器
    :return: 日志记录器对象
    """
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        logger.setLevel(setting.LOG_LEVEL)
        log_format = logging.Formatter(
            '%(levelname)s - %(asctime)s - %(filename)s:%(lineno)d -[%(module)s:%(funcName)s] - %(message)s'
        )
        file_handler = RotatingFileHandler(
            filename=logfile_name,
            mode='a',
            maxBytes=10 * 1024 * 1024,
            backupCount=10,
            encoding='utf-8',
        )
        file_handler.setLevel(setting.LOG_LEVEL)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

        sh = logging.StreamHandler()
        sh.setLevel(setting.STREAM_LOG_LEVEL)
        sh.setFormatter(log_format)
        logger.addHandler(sh)
    return logger


class RecordLog:
    def __init__(self):
        self.handle_overdue_log()
    def handle_overdue_log(self):
        pass

logs = get_log()