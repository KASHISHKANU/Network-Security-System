from datetime import datetime
import numpy as np
import pandas as pd
import os 
import sys

'''
DEFINING ALL THE CONSTANTS THAT ARE GENERALLY USED
'''
TARGET_COLUMN:str = "Result"  # column to be predicted
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "artifact"
FILE_NAME:str = "phisingData.csv"
TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"
SCHEMA_FILE_PATH:str = os.path.join("data_schema","schema.yaml")
SAVED_MODEL_DIR:str = os.path.join("saved_models")
MODEL_FILE_NAME:str = "model.pkl"
'''
DATA INGESTION RELATED CONSTANTS START WITH DATA_INGESTION VARAIBLES
'''
DATA_INGESTION_COLLECTION_NAME: str = "Network_Data_Collection"
DATA_INGESTION_DATABASE_NAME:str = "Network_Security_System"   
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION:float = 0.2

'''
DATA VALIDATION RELATED CONSTANTS START WITH DATA_VALIDATION VARAIBLES
'''
DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR:str = "valided"
DATA_VALIDATION_INVALID_DIR:str = "invalided"
DATA_VALIDATION_DRIFT_REPORT_DIR:str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"

'''
DATA TRANSFORMATION RELATED CONSTANTS START WITH DATA_TRANSFORMATION VARAIBLES
'''
DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"   
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object"
PREPROCESSING_OBJECT_FILE_NAME:str = "preprocessing.pkl"
# knn imputer params to handle missing values
DATA_TRANSFORMATION_IMPUTER_PARAMS = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}

'''
Model Trainer RELATED CONSTANTS START WITH MODEL_TRAINER VARAIBLES
'''
MODEL_TRAINER_DIR_NAME:str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD:float = 0.05
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"

TRAINING_BUCKET_NAME:str = "Network-Security-System"