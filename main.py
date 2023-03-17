from finance_complaint.pipeline.training import TrainingPipeline
from finance_complaint.config.pipeline.training import FinanceConfig

from finance_complaint.exception import FinanceException
from finance_complaint.logger import logging

import os
import sys


if __name__ == '__main__':
    try:
        finance_config = FinanceConfig()
        training_pipeline = TrainingPipeline(finance_config=finance_config)
        training_pipeline.start()
    except Exception as e:
        raise FinanceException(e, sys)
