import os
from textwrap import dedent
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv

# Load environment variables (in case other AWS credentials are needed)
load_dotenv()

def training(**kwargs):
    from networksecurity.pipeline.training_pipeline import TrainingPipeline
    training_obj = TrainingPipeline()
    training_obj.run_pipeline()

def sync_artifact_to_s3_bucket(**kwargs):
    # Hardcoded bucket name and directories based on your input
    bucket_name = "networksecuritymlops"
    artifact_dir = "/app/Artifacts"  # Ensure this matches the directory where artifacts are stored
    saved_model_dir = "/app/saved_models"  # Ensure this matches the directory where models are saved
    
    # Sync artifacts directory
    artifact_sync_command = f"aws s3 sync {artifact_dir} s3://{bucket_name}/artifact"
    sync_artifact_result = os.system(artifact_sync_command)
    if sync_artifact_result != 0:
        raise Exception(f"Failed to sync {artifact_dir} to s3://{bucket_name}/artifact")

    # Sync saved models directory
    saved_model_sync_command = f"aws s3 sync {saved_model_dir} s3://{bucket_name}/saved_models"
    sync_saved_model_result = os.system(saved_model_sync_command)
    if sync_saved_model_result != 0:
        raise Exception(f"Failed to sync {saved_model_dir} to s3://{bucket_name}/saved_models")

# Define the DAG
with DAG(
    'network_training',
    default_args={'retries': 2},
    description='Network security training pipeline with S3 synchronization',
    schedule="@weekly",  # Updated from schedule_interval to schedule for Airflow 3
    start_date=pendulum.datetime(2024, 11, 5, tz="UTC"),
    catchup=False,
    tags=['example'],
) as dag:

    # Task to execute the training pipeline
    training_pipeline = PythonOperator(
        task_id="train_pipeline",
        python_callable=training
    )

    # Task to sync data to S3
    sync_data_to_s3 = PythonOperator(
        task_id="sync_data_to_s3",
        python_callable=sync_artifact_to_s3_bucket
    )

    # Task dependencies
    training_pipeline >> sync_data_to_s3
