from finance_complaint.exception import FinanceException
from finance_complaint.logger import logging

from finance_complaint.components.training.data_ingestion import DataIngestion
from finance_complaint.config.pipeline.training import FinanceConfig
from finance_complaint.entity.artifact_entity import DataIngestionArtifact

import os
import sys


class TrainingPipeline:

    def __init__(self, finanace_config: FinanceConfig):

        self.finance_config = finanace_config

    def start_data_ingestion(self) -> DataIngestionArtifact:

        try:
            data_ingestion_config = self.finance_config.get_data_ingestion_config()
            data_ingestion = DataIngestion(
                data_ingestion_config=data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion artifact {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise FinanceException(e, sys)

    def start(self):

        try:
            data_ingestion_artifact = self.start_data_ingestion()

        except Exception as e:
            raise FinanceException(e, sys)
