
# Network Security - Malicious URL Detection 🚀

This project is a comprehensive end-to-end MLOps pipeline to detect malicious URLs using **XGBoost**. It integrates various tools and techniques to ensure production-grade quality while showcasing best practices in MLOps.

---
## **Project Workflow Overview** 🛠️
![image](https://github.com/user-attachments/assets/95214838-6af5-48d2-b7d7-9ee35a835848)



1. **Data Ingestion**:
   - Fetched data directly from **MongoDB**.
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
   - Ensured that any new model provides measurable improvement before acceptance.

6. **Model Pusher**:
   - Saved the trained model to the **"saved_models"** directory for production deployment.
   - Uploaded the model and related artifacts to **AWS S3** for centralized storage.

---
