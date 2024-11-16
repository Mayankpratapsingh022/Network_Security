
# Network Security - Malicious URL Detection 🚀

This project is a comprehensive end-to-end MLOps pipeline to detect malicious URLs using **XGBoost**. It integrates various tools and techniques to ensure production-grade quality while showcasing best practices in MLOps.

---
## **Project Workflow Overview** 🛠️
![image](https://github.com/user-attachments/assets/95214838-6af5-48d2-b7d7-9ee35a835848)



1. **Data Ingestion**:
   - Fetched data directly from **MongoDB**.
    ![image](https://github.com/user-attachments/assets/ff806462-7b17-48a3-bad1-cd6f2186a72c)
      ```python
      def export_collection_as_dataframe(self):
          try:
              database_name = self.data_ingestion_config.database_name
              collection_name = self.data_ingestion_config.collection_name
      
              with pymongo.MongoClient(MONGO_DB_URL) as mongo_client:
                  collection = mongo_client[database_name][collection_name]
      
                  # Logging to verify if collection has data
                  count = collection.count_documents({})
                  logging.info(f"Number of records retrieved from MongoDB: {count}")
      
                  if count == 0:
                      raise ValueError("No records found in MongoDB collection. Please check the data source.")
      
                  df = pd.DataFrame(list(collection.find()))
                  if "_id" in df.columns.to_list():
                      df = df.drop(columns=["_id"], axis=1)
      
                  df.replace({"na": np.nan}, inplace=True)
                  logging.info(f"Dataframe shape after exporting from MongoDB: {df.shape}")
      
                  return df
      
          except pymongo.errors.PyMongoError as e:
              raise NetworkSecurityException(f"MongoDB error: {str(e)}", sys)
      ```

   - Cleaned the data by replacing missing values (`na`) with `np.nan` and dropping unnecessary columns like `_id`.
   - Exported the processed data to a **feature store** for further usage.
   - Split the data into **training** and **testing** datasets, ensuring no data leakage.

2. **Data Validation**:
   - Validated the schema to ensure all required columns are present.
   - Checked numerical columns for correctness and detected **data drift** using statistical tests.
   - Generated detailed drift reports to monitor dataset consistency.

3. **Data Transformation**:
   - Applied preprocessing steps, such as imputing missing values using a **KNNImputer**.
   - Prepared the data into transformed **NumPy arrays** for model training.
   - Saved the transformation pipeline as an artifact for future use.

4. **Model Training**:
   - Trained an **XGBoost Classifier** on the preprocessed data.
   - Performed overfitting and underfitting checks using metrics like **F1-score**.
   - Saved the trained model along with its preprocessing pipeline as a **pickle file**.

5. **Model Evaluation**:
   - Compared the new model with the existing deployed model (if available).
   - Evaluated metrics such as **Precision**, **Recall**, and **F1-score** using **MLflow** for tracking.
     ![image](https://github.com/user-attachments/assets/33bd60a6-41c5-4d28-9bb2-d3006db91070)
     ![image](https://github.com/user-attachments/assets/09a004b7-5452-4349-81f8-fe54b54208d2)
     - While the model shows signs of overfitting, the primary objective of this project is to demonstrate the implementation of a robust CI/CD pipeline.
      Model optimization can be addressed as a future enhancement.
     ![image](https://github.com/user-attachments/assets/48722274-17b6-40b3-8ce9-1923b0523718)

     


   - Ensured that any new model provides measurable improvement before acceptance.

6. **Model Pusher**:
   - Saved the trained model to the **"saved_models"** directory for production deployment.
   - Uploaded the model and related artifacts to **AWS S3** for centralized storage.
      - "networksecuritymlops" bucket is used to store artifacts and models
         ![image](https://github.com/user-attachments/assets/a2c504a7-1564-481a-8002-e5ae572b9f22)
      - Screenshot of the AWS S3 bucket structure showing organized folders for artifacts and saved models used in the MLOps pipeline.
         ![image](https://github.com/user-attachments/assets/49c4a703-0cb6-4c1f-a3dd-d02bbfad4886)
      - Screenshot of the S3 bucket structure under the `artifact` folder, showcasing organized subdirectories for different pipeline stages such as data ingestion, transformation, validation, model training, and model pusher.
        ![image](https://github.com/user-attachments/assets/a8b04213-43eb-472e-82f9-91c95060484c)
      - Screenshot of the `saved_models` folder in the S3 bucket, containing the final trained model (`model.pkl`) ready for deployment
        ![image](https://github.com/user-attachments/assets/ef5f9516-4396-4f61-b5f1-c6d0395161ea)

           

        




---
