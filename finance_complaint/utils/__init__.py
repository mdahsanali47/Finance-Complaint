import shutil
import os
import sys
import yaml
from typing import List
from pyspark.sql import SparkSession

from finance_complaint.exception import FinanceException


def write_yaml_file(file_path: str, data: dict = None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(data, file)
    except Exception as e:
        raise FinanceException(e, sys)


def read_yaml_file(file_path: str) -> dict:
    """
    Read yaml file
    file_path: str
    """

    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise FinanceException(e, sys)
