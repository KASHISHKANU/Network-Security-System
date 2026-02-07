from networksecurity.entity.artifact_entity import (
    DataIngestionConfigArtifact,
    DataValidationConfigArtifact
)
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utlis import read_yaml_file, write_yaml_file

import os
import sys
import pandas as pd
from scipy.stats import ks_2samp


class DataValidation:
    def __init__(
        self,
        data_validation_config: DataValidationConfig,
        data_ingestion_config_artifact: DataIngestionConfigArtifact
    ):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_config_artifact
            self.schema = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            required_columns = len(self.schema["columns"])
            logging.info(f"Required columns: {required_columns}")
            logging.info(f"Received columns: {len(dataframe.columns)}")
            return len(dataframe.columns) == required_columns
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                ks_result = ks_2samp(d1, d2)
                drift_found = ks_result.pvalue < threshold
                if drift_found:
                    status = False
                report[column] = {
                    "pvalue": float(ks_result.pvalue),
                    "drift_status": bool(drift_found)
                }
            drift_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_path), exist_ok=True)
            write_yaml_file(
                file_path=drift_path,
                content=report,
                replace=True
            )
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationConfigArtifact:
        try:
            error_message = ""
            train_path = self.data_ingestion_artifact.training_file_path
            test_path = self.data_ingestion_artifact.testing_file_path
            train_df = self.read_data(train_path)
            test_df = self.read_data(test_path)
            if not self.validate_number_of_columns(train_df):
                error_message += "Training data column mismatch. "
            if not self.validate_number_of_columns(test_df):
                error_message += "Testing data column mismatch. "
            if error_message:
                raise Exception(error_message)
            validation_status = self.detect_dataset_drift(
                base_df=train_df,
                current_df=test_df
            )
            os.makedirs(
                os.path.dirname(
                    self.data_validation_config.valid_train_file_path
                ),
                exist_ok=True
            ) 
            train_df.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True
            )
            data_validation_artifact = DataValidationConfigArtifact(
                validation_status=validation_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logging.info("Data Validation completed successfully")
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
