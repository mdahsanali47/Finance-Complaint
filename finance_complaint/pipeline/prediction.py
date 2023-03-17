import sys
import os
from typing import List, Tuple
from pyspark.sql import DataFrame

from finance_complaint.config.spark_manager import spark_session

from finance_complaint.exception import FinanceException
from finance_complaint.logger import logging

from finance_complaint.entity.config_entity import PredictionPipelineConfig
from finance_complaint.constant.prediction_pipeline_config.file_config import *
from finance_complaint.constant.model import S3_MODEL_BUCKET_NAME, S3_MODEL_DIR_KEY, MODEL_SAVED_DIR

from finance_complaint.entity.schema import FinanceDataSchema
from finance_complaint.entity.estimator import S3FinanceEstimator

from finance_complaint.cloud_storage import SimpleStorageService


class PredictionPipeline:
    def __init__(self, pipeline_config: PredictionPipelineConfig) -> None:
        pipeline_config = PredictionPipelineConfig()
        self.__pyspark_s3_root = PYSPARK_S3_ROOT
        self.pipeline_config = pipeline_config
        self.s3_storage: SimpleStorageService = SimpleStorageService(s3_bucket_name=S3_DATA_BUCKET_NAME,
                                                                     region_name=pipeline_config.region_name)
        self.schema: FinanceDataSchema = FinanceDataSchema()

    def get_pyspark_s3_file_path(self, dir_path: str) -> str:
        return os.path.join(self.__pyspark_s3_root, dir_path)

    def read_file(self, file_path: str) -> DataFrame:
        try:
            file_path = self.get_pyspark_s3_file_path(file_path)
            df = spark_session.read.parquet(file_path)
            return df.limit(1000)

        except Exception as e:
            raise FinanceException(e, sys)

    def write_file(self, dataframe: DataFrame, file_path: str) -> bool:
        try:

            if file_path.endswith('csv'):
                file_path = os.path.dirname(file_path)

            file_path = self.get_pyspark_s3_file_path(file_path)
            print(file_path)
            logging.info(f"writing parquet file at :{file_path}")

            dataframe.write.parquet(file_path, mode="overwrite")
            return True

        except Exception as e:
            raise FinanceException(e, sys)

    def is_valid_file(self, file_path: str) -> bool:
        try:

            dataframe: DataFrame = self.read_file(file_path)
            columns = dataframe.columns
            misssing_columns = []
            for column in self.schema.required_prediction_columns:
                if column not in columns:
                    misssing_columns.append(column)

            if len(misssing_columns) > 0:
                logging.info(f"Missing columns : {misssing_columns}")
                logging.info(f"existing columns : {columns}")
                return False
            return True

        except Exception as e:
            raise FinanceException(e, sys)

    def get_valid_files(self, file_paths: List[str]) -> Tuple[List[str], List[str]]:
        try:
            valid_file_paths = []
            invalid_file_paths = []
            for file_path in file_paths:
                is_valid = self.is_valid_file(file_path)
                if is_valid:
                    valid_file_paths.append(file_path)
                else:
                    invalid_file_paths.append(file_path)
            return valid_file_paths, invalid_file_paths

        except Exception as e:
            raise FinanceException(e, sys)

    def start_batch_prediction(self):
        try:
            input_dir = self.pipeline_config.input_dir
            files = [input_dir]
            logging.info(f"files : {files}")
            valid_files, invalid_files = self.get_valid_files(files)
            invalid_files = valid_files
            if len(invalid_files) > 0:
                logging.info(
                    f" Invalid files found of length : {len(invalid_files)}")
                failed_dir = self.pipeline_config.failed_dir
                for invalid_file in invalid_files:
                    logging.info(
                        f"moving invalid files {invalid_file} to failed dir :{failed_dir}")
                    # self.s3_storage.move(source_key=invalid_file, destination_dir_key=failed_dir)

            if len(valid_files) == 0:
                logging.info("No valid files found")
                return None

            estimator = S3FinanceEstimator(
                bucket_name=S3_MODEL_BUCKET_NAME, s3_key=S3_MODEL_DIR_KEY)
            for valid_file in valid_files:
                logging.info(f"Prediction of file starting :{valid_file}")
                df: DataFrame = self.read_file(valid_file)
                # df = df.drop(self.schema.col_consumer_disputed)
                transformer_df = estimator.transform(df)
                required_columns = self.schema.required_prediction_columns + \
                    [self.schema.prediction_column_name]
                logging.info(f"Saving required columns : {required_columns}")
                transformer_df = transformer_df.select(required_columns)
                transformer_df.show()
                prediction_file_path = os.path.join(
                    self.pipeline_config.prediction_dir, os.path.basename(valid_file))
                logging.info(
                    f"Saving prediction file at :{prediction_file_path}")
                self.write_file(transformer_df, prediction_file_path)
                archive_file_path = os.path.join(
                    self.pipeline_config.archive_dir, os.path.basename(valid_file))
                logging.info(
                    f"Archiving valid input file at :{archive_file_path}")
                self.write_file(df, archive_file_path)

        except Exception as e:
            raise FinanceException(e, sys)
