import logging
import os
from decouple import config

file_path = config('LOG_PATH')


def log2file():
    """This will set a logging file on a fixed location"""
    if os.path.exists(file_path):
        return logging.basicConfig(filename='./Logs/full.log', encoding='utf-8', level=logging.DEBUG)
    else:
        os.mkdir(file_path)
        return logging.basicConfig(filename='./Logs/full.log', encoding='utf-8', level=logging.DEBUG)
