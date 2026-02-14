import logging
import os
import sys

LOG_LEVEL = logging.DEBUG
STREAM_LOG_LEVEL=logging.DEBUG

DIR_BASE = os.path.dirname(os.path.dirname(__file__))

FILE_PATH = {
    'LOG': os.path.join(DIR_BASE, 'logs')
}