from networksecurity.constants.training_pipeline import MODEL_FILE_NAME,SAVED_MODEL_DIR

import os
import sys

from networksecurity.exception.exception import NetworkSecurityException    
from networksecurity.logging.logger import logging

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def predict(self, X):
        try:
            x_tranform = self.preprocessor.transform(X)
            y_hat = self.model.predict(x_tranform)
            return y_hat 
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def save_model(self, model_dir=SAVED_MODEL_DIR, model_file_name=MODEL_FILE_NAME):
        try:
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, model_file_name)
            with open(model_path, 'wb') as f:
                import pickle
                pickle.dump(self.model, f)
            logging.info(f"Model saved at {model_path}")
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e