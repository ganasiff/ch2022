import logging
import os
from decouple import config

file_path = config('LOG_PATH')
file_name = config('LOG_FILENAME')
file_path_tests = config('LOG_PATH_TESTS')
file_name_tests = config('LOG_FILENAME_TESTS')


def log2file_init():
    """This will setup a logging file on a fixed location provided the conf in .env"""
    if os.path.exists(file_path):
        return logging.basicConfig(filename=f'./Logs/{file_name}', encoding='utf-8', level=logging.DEBUG)
    else:
        os.mkdir(file_path)
        return logging.basicConfig(filename=f'./Logs/{file_name}', encoding='utf-8', level=logging.DEBUG)


def log2file_tests():
    """This will setup a logging file on a fixed location provided the conf in .env"""
    if os.path.exists(file_path_tests):
        return logging.basicConfig(filename=f'./Logs/{file_name_tests}', encoding='utf-8', level=logging.DEBUG)
    else:
        os.mkdir(file_path_tests)
        return logging.basicConfig(filename=f'./Logs/{file_name_tests}', encoding='utf-8', level=logging.DEBUG)
