from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys

if __name__ == "__main__":
    try:
        # Data Ingestion
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
        dataingestion = DataIngestion(data_ingestion_config=dataingestionconfig)
        logging.info("Starting data ingestion")
        dataingestionartifact = dataingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print(dataingestionartifact)

        # Data Validation
        datavalidationconfig = DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
        datavalidation = DataValidation(data_validation_config=datavalidationconfig, data_ingestion_artifact=dataingestionartifact)
        logging.info("Starting data validation")
        datavalidationartifact = datavalidation.initiate_data_validation()
        logging.info("Data validation completed")
        print(datavalidationartifact)  

        # Data Transformation
        data_transformation_config = DataTransformationConfig(training_pipeline_config=trainingpipelineconfig)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config, data_validation_config_artifact=datavalidationartifact)
        logging.info("Starting data transformation")
        datat_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation completed")
        print(datat_transformation_artifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)