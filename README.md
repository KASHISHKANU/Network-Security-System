# 🔐 Network Security System – Phishing Detection

An end-to-end **Machine Learning based Network Security System** to detect **phishing websites** using structured data.  
The project follows a **production-grade ML pipeline architecture** including data ingestion, validation, transformation, training, prediction, and deployment-ready API.

---

## 🚀 Features

- End-to-end ML pipeline (Ingestion → Validation → Transformation → Training)
- Schema-based data validation
- Saved preprocessing & trained model artifacts
- Batch & single prediction support
- Web interface for predictions
- Modular, scalable project structure
- MLflow experiment tracking support

---

## 🧠 Machine Learning Workflow

Raw Data
↓
Data Ingestion
↓
Data Validation (schema.yaml)
↓
Data Transformation (preprocessor.pkl)
↓
Model Training (model.pkl)
↓
Experiment Tracking (MLflow + DAGsHub)
↓
Prediction (API / CSV)

---

## 📂 Project Structure

Network Security System/
│
├── app.py # Web app & prediction API
├── main.py # Training pipeline trigger
├── push_data.py # Push data to database (MongoDB)
├── requirements.txt # Project dependencies
├── setup.py # Package setup
├── README.md
├── mlflow.db # Local MLflow tracking database
│
├── final_models/
│ ├── model.pkl # Trained ML model
│ └── preprocessor.pkl # Data preprocessing pipeline
│
├── data_schema/
│ └── schema.yaml # Data validation schema
│
├── Network_Data/
│ └── phishingData.csv # Raw dataset
│
├── valid_data/
│ └── test.csv # Sample test data
│
├── prediction_output/
│ └── output.csv # Prediction results
│
├── static/
│ ├── css/style.css
│ └── js/effects.js
│
├── template/
│ ├── base.html
│ ├── index.html
│ └── table.html
│
├── networksecurity/
│ ├── components/
│ │ ├── data_ingestion.py
│ │ ├── data_validation.py
│ │ ├── data_transformation.py
│ │ └── model_trainer.py
│ │
│ ├── pipeline/
│ │ └── training_pipeline.py
│ │
│ ├── entity/
│ │ ├── artifact_entity.py
│ │ └── config_entity.py
│ │
│ ├── exception/
│ │ └── exception.py
│ │
│ ├── logging/
│ │ └── logger.py
│ │
│ ├── utils/
│ │ └── ml_utils/
│ │
│ └── constants/
│
└── venv/

---

## ⚙️ Installation & Setup

1️⃣ Clone the Repository
```bash
git clone <https://github.com/KASHISHKANU/Network-Security-System >
cd Network-Security-System

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

---

🔐 DAGsHub + MLflow Setup

This project uses DAGsHub as a remote MLflow tracking server for experiment tracking and artifact management.

1️⃣ Create a DAGsHub Repository
Visit: https://dagshub.com
Create a new repository
Generate an access token

2️⃣ Create .env File
MLFLOW_TRACKING_URI=https://dagshub.com/<username>/<repo-name>.mlflow
MLFLOW_TRACKING_USERNAME=<your-dagshub-username>
MLFLOW_TRACKING_PASSWORD=<your-dagshub-access-token>

3️⃣ Load Environment Variables
source .env          # Linux / Mac

or on Windows:
setx MLFLOW_TRACKING_URI "https://dagshub.com/..."

---

🏗️ Train the Model

Run the complete training pipeline:
python main.py

- This will generate:
1. final_models/model.pkl
2. final_models/preprocessor.pkl

---

🌐 Run the Application
python app.py
Open browser at: http://localhost:5000

- You can:
1. Upload CSV files
2. Get batch predictions
3. View results in tabular format

---

🔍 Prediction Logic

1. Input data is loaded
2. preprocessor.pkl transforms the data
3. model.pkl predicts phishing / legitimate
4. Output is saved to prediction_output/output.csv

---

📊 MLflow Tracking (Optional)

- MLflow is used for:
1. Experiment tracking
2. Model metrics logging
3. Artifact management

Tracking DB: mlflow.db

--- 

🧪 Sample Test 

Use:
valid_data/test.csv (for testing predictions)

---

🛡️ Tech Stack

1.  Python
2.  Scikit-learn
3.  Pandas / NumPy
4.  MLflow
5.  Flask / FastAPI
6.  HTML / CSS / JavaScript
7.  MongoDB (optional)
8.  Machine Learning 
9.  Models --> Adaboost, Random-Forest, Decision-Tree, Gradient-Boosting, Logistic-Regression
10. DAGsHub (Remote Experiment Tracking & MLOps)
11. MLOps

---

📌 Use Case

1. Phishing website detection
2. Network security analytics
3. Cybersecurity ML systems
4. End-to-end MLOps projects

---

👨‍💻 Author

Kashish Raj
B.Tech | Machine Learning | Network Security 
GitHub & LinkedIn linked in profile

---

