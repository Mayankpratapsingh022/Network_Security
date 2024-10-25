import sys  
import os  
import numpy as np 
import pandas as pd  
from sklearn.impute import KNNImputer 
from sklearn.pipeline import Pipeline  

from networksecurity.constant.training_pipeline import TARGET_COLUMN 
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS 
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact,
)

from networksecurity.entity.config_entity import DataTransformationConfig 
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logger.logger import logging  
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object





class DataTransformation:
    def __init__(self):
        pass