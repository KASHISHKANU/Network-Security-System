from datetime import datetime
import numpy as np
import pandas as pd
import os 
import sys

'''
DEFINING ALL THE CONSTANTS RELATED TO TRAINING PIPELINE
'''
TARGET_COLUMN:str = "Result"  # column to be predicted
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "artifact"
FILE_NAME:str = "phisingData.csv"
TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"
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