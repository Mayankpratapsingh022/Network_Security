from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging


#configuration of component and artifact generation
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import pandas as pd
import numpy as np
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_collection_as_dataframe(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)

            return df
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            # Check if the dataframe is empty
            if dataframe.empty:
                raise ValueError("The DataFrame is empty. Cannot perform train-test split.")

            # Check if the number of rows is sufficient for splitting
            if len(dataframe) < 2:
                raise ValueError("The DataFrame does not have enough rows to perform a train-test split.")

            # Set a default test size if none is provided
            test_size = self.data_ingestion_config.train_test_split_ratio
            if test_size is None or not (0 < test_size < 1):
                test_size = 0.2
            logging.info(f"Using test size: {test_size}")

            # Perform the train-test split
            train_set, test_set = train_test_split(
                dataframe, test_size=test_size, random_state=42
            )
            logging.info("Performed train-test split on the dataframe")

            # Save the train and test sets
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            
            logging.info(f"Exported train and test file paths: {self.data_ingestion_config.training_file_path}, {self.data_ingestion_config.testing_file_path}")
            
        except ValueError as e:
            raise NetworkSecurityException(f"Value error: {str(e)}", sys)
        except OSError as e:
            raise NetworkSecurityException(f"File system error: {str(e)}", sys)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            
            # Check if the dataframe is empty before proceeding
            if dataframe.empty:
                raise ValueError("Data ingestion failed. The DataFrame is empty after fetching data from MongoDB. Please check the data source.")
            
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe=dataframe)
            
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return data_ingestion_artifact
        except ValueError as e:
            logging.error(f"Value error during data ingestion: {e}")
            raise NetworkSecurityException(e, sys)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
