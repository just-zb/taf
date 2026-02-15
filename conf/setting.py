import logging
import os
import sys
from pathlib import Path

LOG_LEVEL = logging.DEBUG
STREAM_LOG_LEVEL=logging.DEBUG

DIR_BASE = Path(__file__).resolve().parent.parent

# 接口超时时间，单位/s
API_TIMEOUT = 60

FILE_PATH = {
    'LOG': DIR_BASE/ 'logs',
    'CONFIG': DIR_BASE / 'conf/config.ini',
    'EXTRACT': DIR_BASE / 'extract.yaml',
}