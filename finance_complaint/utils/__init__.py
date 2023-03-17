import shutil
import os
import sys
import yaml
from typing import List

from pyspark.sql import DataFrame
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

from finance_complaint.exception import FinanceException
from finance_complaint.logger import logging


def write_yaml_file(file_path: str, data: dict = None):
    """
    Create yaml file
    file_path: str
    data: dict
    """

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            if data is not None:
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


def get_score(dataframe: DataFrame, metric_name, label_col, prediction_col) -> float:
    try:
        evaluator = MulticlassClassificationEvaluator(
            labelCol=label_col,
            predictionCol=prediction_col,
            metricName=metric_name)

        score = evaluator.evaluate(dataframe)
        print(f"{metric_name} score = {score}")
        logging.info(f"{metric_name} score = {score}")
        return score
    except Exception as e:
        raise FinanceException(e, sys)

