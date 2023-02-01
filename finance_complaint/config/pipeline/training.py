from finance_complaint.exception import FinanceException
from finance_complaint.logger import logging

from finance_complaint.constant.training_pipeline_config import *
from finance_complaint.constant import *

from finance_complaint.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from finance_complaint.entity.metadata_entity import DataIngestionMetadata
import os
import sys


class FinanceConfig:

    def __init__(self, pipeline_name=PIPELINE_NAME, timestamp=TIMESTAMP):
        self.pipeline_name = pipeline_name
        self.timestamp = timestamp
        self.pipeline_config = self.get_pipeline_config()

    def get_pipeline_config(self) -> TrainingPipelineConfig:
        """
        This function will provide pipeline config information
        returns > PipelineConfig = namedtuple("PipelineConfig", ["pipeline_name", "artifact_dir"])
        """
        try:

            artifact_dir = PIPELINE_ARTIFACTS_DIR
            pipelline_config = TrainingPipelineConfig(
                self.pipeline_name, artifact_dir)

            logging.info(f"Pipeline config : {pipelline_config}")
            return pipelline_config
        except FinanceException as e:
            raise FinanceException(e, sys)

    def get_data_ingestion_config(self, from_date=DATA_INGESTION_MIN_START_DATE,
                                  to_date=None) -> DataIngestionConfig:
        """
        This function will provide data ingestion config information
        returns > DataIngestionConfig

        - from date can not be less than min start date
        - if to_date is not provided automatically current date will become to date

        """
        try:
            min_start_date = datetime.strptime(
                DATA_INGESTION_MIN_START_DATE, "%Y-%m-%d")
            from_date_obj = datetime.strptime(
                to_date, "%Y-%m-%d")

            if from_date_obj < min_start_date:
                from_date = DATA_INGESTION_MIN_START_DATE
            if to_date is None:
                to_date = datetime.now().strftime("%Y-%m-%d")

            """
            master directory for data ingestion
            we will store metadata information and ingested file to avoid redundant download
            """
            data_ingestion_master_dir = os.path.join(
                self.pipeline_config.artifact_dir, DATA_INGESTION_DIR)

            # time based directory for data ingestion in each run:
            data_ingestion_dir = os.path.join(
                data_ingestion_master_dir, self.timestamp)

            # metadata file path
            metadata_file_path = os.path.join(
                data_ingestion_master_dir, DATA_INGESTION_METADATA_FILE_NAME)

            data_ingestion_metadata = DataIngestionMetadata(
                metadata_file_path=metadata_file_path)

            if data_ingestion_metadata.is_metadata_file_present:
                metadata_info = data_ingestion_metadata.get_metadata_info()
                from_date = metadata_info.to_date

            data_ingestion_config = DataIngestionConfig(
                from_date=from_date,
                to_date=to_date,
                data_ingestion_dir=data_ingestion_dir,
                download_dir=os.path.join(
                    data_ingestion_dir, DATA_INGESTION_DOWNLOAD_DIR),
                file_name=DATA_INGESTION_FILE_NAME,
                feature_store_dir=os.path.join(
                    data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR),
                failed_dir=os.path.join(
                    data_ingestion_dir, DATA_INGESTION_FAILED_DIR),
                metadata_file_path=metadata_file_path,
                datasource_url=DATA_INGESTION_DATA_SOURCE_URL)

            logging.info(f"Data ingestion config : {data_ingestion_config}")
            return data_ingestion_config

        except FinanceException as e:
            raise FinanceException(e, sys)
