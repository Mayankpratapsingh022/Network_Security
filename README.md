
# Network Security - Malicious URL Detection using MLOps

This repository presents a comprehensive end-to-end MLOps project designed to detect malicious URLs using XGBoost, ensuring user safety by identifying harmful links through machine learning. The project integrates a variety of tools and best practices to build a robust, scalable, and production-grade MLOps pipeline. By combining data ingestion, model training, deployment, and monitoring, it provides a complete solution for real-time and batch URL safety assessments.

---

## Introduction

Malicious URLs are links that lead to harmful websites, often used by cybercriminals through phishing emails, social engineering, and other tactics. This project detects malicious URLs using machine learning and provides both single URL predictions and batch predictions through an interactive UI.

---

![artitecture main](https://github.com/user-attachments/assets/3811845a-ab90-4257-a1f7-fb9da2f98015)





## **Tech Stack** 🛠️

| **Category**             | **Tools/Technologies**                                  | **Description**                                                |
|--------------------------|---------------------------------------------------------|----------------------------------------------------------------|
| **Frontend**             | Streamlit                                               | Provides a simple UI for real-time single URL predictions.     |
| **Backend**              | FastAPI                                                 | Handles batch predictions and API endpoints.                   |
| **Modeling**             | XGBoost, Python                                         | Machine learning model for detecting malicious URLs.           |
| **Database**             | MongoDB                                                 | Stores data records for ingestion and model training.          |
| **Orchestration**        | Apache Airflow                                          | Orchestrates training, retraining, and batch prediction pipelines. |
| **Experiment Tracking**  | MLflow                                                  | Tracks model metrics like F1-score, Precision, and Recall.     |
| **CI/CD**                | GitHub Actions                                          | Automates CI/CD pipelines, including Docker build and deployment. |
| **Containerization**     | Docker, AWS ECR                                         | Docker images stored securely in **ECR** for consistent deployment. |
| **Cloud Storage**        | AWS S3                                                  | Stores artifacts, trained models, and logs.                    |
| **Cloud Hosting**        | AWS EC2 Instance                                        | Serves as a **self-hosted runner** for GitHub Actions, enabling deployment. |

---


## **Highlights** 🌟

- **Real-time Single URL Predictions**: Users can interact with the model via a **Streamlit** app to get instant safety assessments.
- **Batch Predictions for Large Datasets**: Handle multiple URLs at once through **FastAPI** for efficient bulk predictions.
- **End-to-End MLOps Pipeline**: Covers data ingestion, transformation, validation, model training, and evaluation, ensuring a robust workflow.
- **Model Retraining Pipeline**: Retrain models manually or through **Apache Airflow**, ensuring the model stays up-to-date with new data.
- **Metrics Tracking with MLflow**: All experiments are tracked with **MLflow** for easy comparison and monitoring.
- **Artifact & Model Storage**: Models and intermediate artifacts are stored securely in **AWS S3**, with deployment readiness at every step.
- **Deployment-Ready Model**: Models are exposed via **FastAPI** and **Streamlit** for end-user interaction.
- **Version Control for Data**: Tracks data schema and detects any drift to maintain high data quality.
- **CI/CD Pipeline**: Fully automated using **GitHub Actions**, with Docker images pushed to **Amazon ECR** and deployed to **AWS EC2**.

---


## Dataset and Features

The dataset contains **30 features** extracted from URLs, which help classify them as **Malicious** or **Safe**.

### Key Features

| **Feature Name**           | **Description**                                                                                   |
|----------------------------|---------------------------------------------------------------------------------------------------|
| `having_IP_Address`        | Checks if the URL contains an IP address instead of a domain name, which can be a sign of phishing.|
| `URL_Length`               | Measures the length of the URL; longer URLs are often used to hide malicious content.            |
| `Shortening_Service`       | Detects the use of URL shortening services like `bit.ly`, often used to disguise harmful links.  |
| `having_At_Symbol`         | Flags the presence of '@' in the URL, which is sometimes used to obscure the real destination.   |
| `double_slash_redirecting` | Identifies if there are multiple slashes after the protocol, which can indicate redirection.     |
<details>
   
  <summary>Click here to expand and view all features</summary>
  

| **Feature Name**           | **Description**                                                                                   |
|----------------------------|---------------------------------------------------------------------------------------------------|
| `Prefix_Suffix`            | Checks for the use of dashes ('-') in the domain, commonly used in phishing URLs to spoof legit domains. |
| `having_Sub_Domain`        | Counts the number of subdomains; excessive subdomains are often used to make a URL appear legitimate. |
| `SSLfinal_State`           | Analyzes the SSL certificate; no SSL or a self-signed certificate may indicate an unsafe URL.    |
| `Domain_registration_length` | Measures the duration of domain registration; shorter registration lengths are common for malicious sites. |
| `Favicon`                  | Checks the favicon’s source; a mismatch between favicon and domain may indicate phishing.        |
| `port`                     | Detects if any unusual ports are being used, which can indicate malicious activity.             |
| `HTTPS_token`              | Flags the use of 'HTTPS' as part of the domain name, which could be a misleading tactic.         |
| `Request_URL`              | Checks if resources (e.g., images, scripts) are loaded from different domains, which may be suspicious. |
| `URL_of_Anchor`            | Analyzes the percentage of anchors (`<a>` tags) pointing to a different domain.                  |
| `Links_in_tags`            | Measures links found inside certain HTML tags like `<meta>`, `<script>`, and `<link>`.           |
| `SFH` (Server Form Handler) | Checks if the form action points to suspicious locations, which could indicate data theft.      |
| `Submitting_to_email`      | Flags URLs that allow form data to be directly submitted to an email, a sign of a phishing attempt.|
| `Abnormal_URL`             | Identifies URLs that do not match their domain, suggesting a discrepancy between URL and content.|
| `Redirect`                 | Counts the number of redirections (`3xx` responses); excessive redirects may indicate phishing.  |
| `on_mouseover`             | Detects if JavaScript `onmouseover` events are being used to change the link destination, tricking users.|
| `RightClick`               | Identifies if right-clicking is disabled, which may indicate attempts to prevent users from inspecting elements.|
| `popUpWindow`              | Flags the presence of pop-up windows, often used for deceptive ads or malicious content.        |
| `Iframe`                   | Detects the presence of invisible iframes, which are often used to load malicious content silently.|
| `age_of_domain`            | Analyzes the domain age; new domains are often used for malicious activities.                   |
| `DNSRecord`                | Checks if the domain has missing DNS records, indicating an untrustworthy website.              |
| `web_traffic`              | Measures the website's traffic volume; low or no traffic may indicate a potentially dangerous URL. |
| `Page_Rank`                | Checks the page rank of the URL; low rank could mean it is not a well-known or trusted source.  |
| `Google_Index`             | Identifies if the URL is indexed by Google; non-indexed URLs might be suspicious.                |
| `Links_pointing_to_page`   | Counts links pointing to the webpage; few or no inbound links may indicate a new or untrustworthy website.|
| `Statistical_report`       | Flags URLs reported for suspicious activity or listed in blacklists.                             |

</details>




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

           

        

## Github Actions 

### **CI/CD Pipeline Overview with GitHub Actions**

The **CI/CD pipeline** is the backbone of this project, automating the processes of integration, delivery, and deployment to streamline the development lifecycle. Using **GitHub Actions**, to ensure that every code update triggers a set of automated workflows to test, build, and deploy the application efficiently and reliably.

![image](https://github.com/user-attachments/assets/9ad3f8c5-9b85-4d89-8bf3-3662bbca22f1)

#### **Continuous Integration**
- Ensures the codebase is always in a deployable state by running unit tests, linting, and other quality checks.
- This step catches errors early in the development cycle, saving time and ensuring code quality.
  
  ![image](https://github.com/user-attachments/assets/d778a287-794d-456f-a9b2-68ac3362ac20)


#### **Continuous Delivery**
- Builds, tags, and pushes the Docker image to **Amazon Elastic Container Registry (ECR)** after successful integration.
- Automates utility installations, AWS configurations, and ECR logins to make the image ready for deployment.
  
  ![image](https://github.com/user-attachments/assets/8058ce67-127e-4de6-ac81-a6368da9198b)


#### **Continuous Deployment**
- Deploys the latest Docker image to an **AWS EC2 instance** for production use.
- Includes the following steps:
  - **Pull Latest Images**: Fetches the most recent Docker image from **Amazon ECR**.
  - **Run Docker Image**: Starts the Docker container with the latest image.
  - **Clean Previous Containers**: Removes outdated images and containers to optimize storage and performance.

  ![image](https://github.com/user-attachments/assets/6ff3eb07-0a97-4980-9112-d3c56c8d381e)






---


### **How to Run** 💻

1. **Data Ingestion**:
   - Start by fetching data from MongoDB using the `data_ingestion` module.

2. **Pipeline Execution**:
   - Use **Airflow DAGs** (`network_training_dag.py` and `network_prediction_dag.py`) for orchestrating training and prediction.

3. **Batch Prediction**:
   - Run the **FastAPI** server to upload a CSV file and receive predictions in JSON format.

4. **Single Prediction**:
   - Launch the **Streamlit** app for real-time prediction of a single URL.

5. **Monitoring**:
   - Track all experiments and metrics via the **MLflow UI**.

