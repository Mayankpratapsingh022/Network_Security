import sys
import os
import certifi
from dotenv import load_dotenv
import pymongo
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from uvicorn import run as app_run
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME, SAVED_MODEL_DIR
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import ModelResolver
from networksecurity.utils.main_utils.utils import load_object

# Load environment variables
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Configure AWS environment variables
os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY

# MongoDB client setup
ca = certifi.where()
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# FastAPI app setup
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jinja2 template setup
templates = Jinja2Templates(directory="templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        print("Starting the training pipeline...")
        train_pipeline = TrainingPipeline()
        if train_pipeline.is_pipeline_running:
            print("Training pipeline is already running.")
            return Response(content="Training pipeline is already running.", media_type="text/html")
        
        train_pipeline.run_pipeline()
        print("Training successful!")
        return Response(content="Training successful!", media_type="text/html")
    except Exception as e:
        print(f"Training failed: {e}")
        raise NetworkSecurityException(e, sys)

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        print("Reading uploaded CSV file...")
        df = pd.read_csv(file.file)
        print("CSV file loaded successfully.")
        
        # Model loading
        model = ModelResolver(model_dir=SAVED_MODEL_DIR)
        latest_model_path = model.get_best_model_path()
        print(f"Loading model from path: {latest_model_path}")
        latest_model = load_object(file_path=latest_model_path)
        
        # Making predictions
        print("Making predictions...")
        y_pred = latest_model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(-1, 0, inplace=True)
        
        return df.to_json()
      
    except Exception as e:
        print(f"Prediction failed: {e}")
        raise NetworkSecurityException(e, sys)
if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)
