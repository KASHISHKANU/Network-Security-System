from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging 

# configuration of data ingestion component
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionConfigArtifact 

import os 
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        # Read the data from MongoDB collection and load it into a pandas DataFrame
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            # Fetching all the data from MongoDB collection and converting it to a pandas DataFrame
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df = df.drop(columns=["_id"], axis=1)
            # replacing "na" string values with np.nan values to recognize missing values
            df.replace({"na":np.nan}, inplace=True)
            return df
        except Exception as e: 
            raise NetworkSecurityException(e, sys)
        
    def export_data_to_feature_store(self, df:pd.DataFrame)->pd.DataFrame:
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)
            df.to_csv(feature_store_file_path, index=False,header=True)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_data_as_train_test(self, df:pd.DataFrame)->None:
        logging.info("Started splitting data into train and test set")
        try:
            logging.info("Started splitting data into train and test set")
            train_set, test_set = train_test_split(
                df,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42
            )
            logging.info("Successfully split the data into train and test set")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            logging.info("Created directory for train and test file")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact = DataIngestionConfigArtifact(
                training_file_path = self.data_ingestion_config.training_file_path,
                testing_file_path = self.data_ingestion_config.testing_file_path
            )
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)