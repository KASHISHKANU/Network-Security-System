import os
import sys
import certifi
import pandas as pd
import pymongo

from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run

from networksecurity.constants.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME
)
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utlis import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


load_dotenv()
ca = certifi.where()
mongo_db_url = os.getenv("MONGO_DB_URL")

client = None
if mongo_db_url:
    client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
    database = client[DATA_INGESTION_DATABASE_NAME]
    collection = database[DATA_INGESTION_COLLECTION_NAME]


app = FastAPI(title="Network Security AI System")

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="./template")


@app.get("/")
async def index(request: Request):
    """Landing UI page"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get("/train")
async def train_route():
    """Local training endpoint (AWS removed)"""
    if os.getenv("ENV") == "production":
        return Response("Training disabled in production", status_code=403)

    train_pipeline = TrainingPipeline()
    train_pipeline.run_pipeline()
    return Response("Training successful")


@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    """Batch prediction with UI rendering"""
    try:
        df = pd.read_csv(file.file)

        preprocessor = load_object("final_models/preprocessor.pkl")
        model = load_object("final_models/model.pkl")

        network_model = NetworkModel(
            preprocessor=preprocessor,
            model=model
        )

        y_pred = network_model.predict(df)
        df["predicted_column"] = y_pred

        os.makedirs("prediction_output", exist_ok=True)
        output_path = "prediction_output/output.csv"
        df.to_csv(output_path, index=False)

        table_html = df.to_html(
            classes="table table-striped table-hover",
            index=False
        )

        return templates.TemplateResponse(
            "table.html",
            {
                "request": request,
                "table": table_html,
                "rows": len(df)
            }
        )

    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


@app.get("/download")
async def download_predictions():
    """Download prediction CSV"""
    file_path = "prediction_output/output.csv"
    if not os.path.exists(file_path):
        return Response("No prediction file found", status_code=404)

    return FileResponse(
        path=file_path,
        filename="network_security_predictions.csv",
        media_type="text/csv"
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app_run(app, host="0.0.0.0", port=port)
