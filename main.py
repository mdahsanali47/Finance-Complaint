from finance_complaint.pipeline.training import TrainingPipeline

from finance_complaint.exception import FinanceException
from finance_complaint.logger import logging

import os
import sys


if __name__ == '__main__':
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.start()
    except Exception as e:
        raise FinanceException(e, sys)
