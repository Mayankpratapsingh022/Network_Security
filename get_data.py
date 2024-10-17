import os
import sys
import json

from dotenv import load_dotenv


import pandas as pd
import numpy as np 
import pymongo 

load_dotenv()
MONGO_DB_URL=os.getenv('MONGO_DB_URL')
#print(MONGO_DB_URL)

import certifi
ca = certifi.where()



from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logger.logger import logging 




class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def csv_tojson_convertor(self,file_path):
        try:
            data =pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def pushing_data_to_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection= collection
            self.records =records 

            self.mongo_client =  pymongo.MongoClient(MONGO_DB_URL)

            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)



            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

if __name__ == '__main__':
    FILE_PATH="./Data/NetworkData.csv"
    DATABASE = "MLOPS_NETWORK_SECURITY"
    COLLECTION = 'NetworkData'

    networkojb =  NetworkDataExtract()
    records = networkojb.csv_tojson_convertor(FILE_PATH)
    no_of_records = networkojb.pushing_data_to_mongodb(records,DATABASE,COLLECTION)

    print(no_of_records)

