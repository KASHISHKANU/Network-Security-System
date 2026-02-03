from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
        dataingestion = DataIngestion(data_ingestion_config=dataingestionconfig)
        logging.info("Starting data ingestion")
        dataingestionartifact = dataingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print(dataingestionartifact)
        datavalidationconfig = DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        datavalidation = DataValidation(data_validation_config=datavalidationconfig, data_ingestion_artifact=dataingestionartifact)
        logging.info("Starting data validation")
        datavalidationartifact = datavalidation.initiate_data_validation()
        logging.info("Data validation completed")
        print(datavalidationartifact)  
    except Exception as e:
        raise NetworkSecurityException(e, sys)