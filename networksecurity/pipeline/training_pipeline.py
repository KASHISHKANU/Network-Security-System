import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig, 
    DataIngestionConfig, 
    DataValidationConfig, 
    DataTransformationConfig, 
    ModelTrainerConfig
)

from networksecurity.entity.artifact_entity import (
    DataIngestionConfigArtifact, 
    DataValidationConfigArtifact, 
    DataTransformationConfigArtifact, 
    ModelTrainerConfigArtifact
)

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Data Ingestion Started")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_config_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion Completed and Artifact: {data_ingestion_config_artifact}")
            return data_ingestion_config_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_config_artifact: DataIngestionConfigArtifact):
        try:
            self.data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Data Validation Started")
            data_validation = DataValidation(data_validation_config=self.data_validation_config,
                                             data_ingestion_config_artifact=data_ingestion_config_artifact)
            data_validation_config_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation Completed and Artifact: {data_validation_config_artifact}")
            return data_validation_config_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def start_data_transformation(self, data_validation_config_artifact: DataValidationConfigArtifact):
        try:
            self.data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Data Transformation Started")
            data_transformation = DataTransformation(data_transformation_config=self.data_transformation_config,
                                                     data_validation_config_artifact=data_validation_config_artifact)
            data_transformation_config_artifact = data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation Completed and Artifact: {data_transformation_config_artifact}")
            return data_transformation_config_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def start_model_trainer(self, data_transformation_config_artifact: DataTransformationConfigArtifact):
        try:
            self.model_trainer_config = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Model Trainer Started")
            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config,
                                         data_transformation_config_artifact=data_transformation_config_artifact)
            model_trainer_config_artifact = model_trainer.initiate_model_trainer()
            logging.info(f"Model Trainer Completed and Artifact: {model_trainer_config_artifact}")
            return model_trainer_config_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
    def run_pipeline(self):
        try:
            data_ingestion_config_artifact = self.start_data_ingestion()
            data_validation_config_artifact = self.start_data_validation(data_ingestion_config_artifact=data_ingestion_config_artifact)
            data_transformation_config_artifact = self.start_data_transformation(data_validation_config_artifact=data_validation_config_artifact)
            model_trainer_config_artifact = self.start_model_trainer(data_transformation_config_artifact=data_transformation_config_artifact)
            logging.info(f"Training Pipeline Completed and Artifact: {model_trainer_config_artifact}")
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
        
        
    
