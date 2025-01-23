"""
file_manager module define two functions
    get_file_path()
    write_json_file()
"""

import json
import os

current_directory = os.getcwd()
SUB_DIRECTORY = "sample"
DIRECTORY_PATH = os.path.join(current_directory, SUB_DIRECTORY)


# 디렉토리가 존재하지 않으면 생성
if not os.path.exists(DIRECTORY_PATH):
    os.makedirs(DIRECTORY_PATH)

FILE_NAME = "sample.json"
FE_TEST_FILE_NAME = "fe_test.json"


def get_file_path():
    """
    get_file_path return current_directory / file_name
    """
    return os.path.join(DIRECTORY_PATH, FILE_NAME)


def get_fe_test_file_path():
    """
    get_fe_test_file_path return current_directory / file_name
    """
    return os.path.join(DIRECTORY_PATH, FE_TEST_FILE_NAME)


def write_json_file(quiz_data, file_path):
    """
    Write JSON data to a file.

    Args:
        json_data (dict): JSON data to be written.
        file_path (str): Path to the file where JSON data will be written.
    """
    with open(file_path, "w", encoding="utf-8") as json_file:
        json_dump = json.dumps(quiz_data, indent=4, ensure_ascii=False)
        json_file.write(json_dump)


def read_json_file():
    file_path = get_file_path()
    with open(file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data
