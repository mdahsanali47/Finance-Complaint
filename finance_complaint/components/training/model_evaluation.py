import os
import sys

from finance_complaint.exception import FinanceException
from finance_complaint.logger import logging

from finance_complaint.entity.artifact_entity import ModelEvaluationArtifact, DataValidationArtifact, ModelTrainerArtifact
from finance_complaint.config.pipeline.training import FinanceConfig
from finance_complaint.entity.config_entity import ModelEvaluationConfig
from finance_complaint.entity.schema import FinanceDataSchema
from finance_complaint.entity.estimator import S3FinanceEstimator

from pyspark.sql.types import StringType,  StructField, StructType, FloatType
from pyspark.sql import DataFrame
from finance_complaint.config.spark_manager import spark_session
from pyspark.ml.feature import StringIndexerModel
from pyspark.ml.pipeline import PipelineModel

from finance_complaint.utils import get_score

from finance_complaint.data_access.model_eval_artifact import ModelEvaluationArtifactData


class ModelEvaluation:

    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact,
                 model_evaluation_config: ModelEvaluationConfig,
                 schema=FinanceDataSchema()):

        try:
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_evaluation_config = model_evaluation_config
            self.schema = schema
            self.bucket_name = self.model_evaluation_config.bucket_name
            self.s3_model_dir_key = self.model_evaluation_config.model_dir
            self.s3_finanace_estimator = S3FinanceEstimator(bucket_name=self.bucket_name,
                                                            s3_key=self.s3_model_dir_key)

            self.metric_reoport_schema = StructType([
                StructField("model_accepted", StringType()),
                StructField("changed-accuracy", FloatType()),
                StructField("trained_model_path", StringType()),
                StructField("besy_model_path", StringType()),
                StructField("active", StringType()),

            ])
            self.model_evaluation_artifact_data = ModelEvaluationArtifactData()

        except Exception as e:
            raise FinanceException(e, sys)

    def read_data(self) -> DataFrame:
        try:
            file_path = self.data_validation_artifact.accepted_file_path
            dataframe: DataFrame = spark_session.read.parquet(file_path)
            return dataframe
        except Exception as e:
            raise FinanceException(e, sys)

    def evaluate_trained_model(self) -> ModelEvaluationArtifact:
        try:
            is_model_accepted = False
            is_active = False

            trained_model_file_path = self.model_trainer_artifact.model_trainer_ref_artifact.trained_model_file_path
            label_indexer_model_path = self.model_trainer_artifact.model_trainer_ref_artifact.label_indexer_model_file_path

            label_indexer_model = StringIndexerModel.load(
                label_indexer_model_path)
            trained_model = PipelineModel.load(trained_model_file_path)

            dataframe: DataFrame = self.read_data()
            dataframe = label_indexer_model.transform(dataframe)

            best_model_path = self.s3_finanace_estimator.get_latest_model_path()
            trained_model_dataframe = trained_model.transform(dataframe)
            best_model_dataframe = self.s3_finanace_estimator.transform(
                dataframe)

            trained_model_f1_score = get_score(dataframe=trained_model_dataframe, metric_name='f1',
                                               label_col=self.schema.target_indexed_label,
                                               prediction_col=self.schema.prediction_column_name)

            best_model_f1_score = get_score(dataframe=best_model_dataframe, metric_name='f1',
                                            label_col=self.schema.target_indexed_label,
                                            prediction_col=self.schema.prediction_column_name)

            logging.info(
                f"trained_model_f1_score {trained_model_f1_score}, Best model f1 score {best_model_f1_score}")

            changed_accuracy = (trained_model_f1_score - best_model_f1_score)

            if changed_accuracy >= self.model_evaluation_config.threshold:
                is_model_accepted = True
                is_active = True

            model_evaluation_artifact = ModelEvaluationArtifact(
                model_accepted=is_model_accepted,
                active=is_active,
                trained_model_path=trained_model_file_path,
                best_model_path=best_model_path,
                changed_accuracy=changed_accuracy
            )
            return model_evaluation_artifact

        except Exception as e:
            raise FinanceException(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            model_accepted = True
            is_active = True

            if not self.s3_finanace_estimator.is_model_available(key=self.s3_finanace_estimator.s3_key):
                latest_model_path = None
                trained_model_path = self.model_trainer_artifact.model_trainer_ref_artifact.trained_model_file_path
                model_evaluation_artifact = ModelEvaluationArtifact(
                    model_accepted=model_accepted,
                    active=is_active,
                    changed_accuracy=0.0,
                    trained_model_path=trained_model_path,
                    best_model_path=latest_model_path

                )
            else:
                model_evaluation_artifact = self.evaluate_trained_model()

            logging.info(f"Model Evaluation Artifact {model_evaluation_artifact}")
            self.model_evaluation_artifact_data.save_eval_artifact(model_eval_artifact=model_evaluation_artifact)
            return model_evaluation_artifact
        except Exception as e:
            raise FinanceException(e, sys)
