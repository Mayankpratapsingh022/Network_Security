from dataclasses import dataclass 
import os 
from networksecurity.constant import training_pipeline



@dataclass 
class DataIngestionArtifact:
    pass 


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
class MOdleEvaluationArtifact:
    pass 


@dataclass 
class ModelPusherArtifact: 
    pass 




@dataclass 
class ClassificationMetricArtifact:
    pass 

