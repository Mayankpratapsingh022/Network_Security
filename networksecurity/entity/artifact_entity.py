from dataclasses import dataclass 
import os 
from networksecurity.constant import training_pipeline



@dataclass 
class DataIngestionArtifact:
    trained_file_path: str 
    test_file_path: str




@dataclass
class DataValidationArtifact:
    pass 


@dataclass 
class DataTransformationArtifact:
    pass 


@dataclass
class ModelTrainerArtifact: 
    pass 


@dataclass 
class ModelEvaluationArtifact:
    pass 


@dataclass 
class ModelPusherArtifact: 
    pass 




@dataclass 
class ClassificationMetricArtifact:
    pass 

