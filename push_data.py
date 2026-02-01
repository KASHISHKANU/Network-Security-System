import os 
import json 
from dotenv import load_dotenv 
import sys

load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()
import pandas as pd
import pymongo
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(selof):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    # Read all the data from Network_Data and convert it into JSON format
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True) # dont want Index column in JSON file
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_to_mongodb(self, records, database, collections): # collection is like table in SQL
        try:
            self.database = database
            self.collections = collections
            self.records = records
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            self.collections = self.database[self.collections]
            self.collections.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
if __name__ == "__main__":
    try:
        file_path = "Network_Data\phisingData.csv"
        database = "Network_Security_System"
        collections = "Network_Data_Collection"
        network_obj = NetworkDataExtract()
        records = network_obj.csv_to_json_convertor(file_path=file_path)
        num_records = network_obj.insert_data_to_mongodb(records, database, collections)
        print(records)
        print(f"Number of records inserted to MongoDB: {num_records}")
        logging.info(f"Number of records inserted to MongoDB: {num_records}")
    except Exception as e:
        raise NetworkSecurityException(e, sys) 
