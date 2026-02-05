import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
import yaml # used for reading yaml files
import dill # used for piclking the files
import numpy as np
import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score

def read_yaml_file(file_path:str) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.
    file_path: str: Path to the YAML file.
    return: dict: Contents of the YAML file.
    """
    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def write_yaml_file(file_path:str, content:object, replace:bool=False)->None:
    """
    Writes a dictionary to a YAML file.
    file_path: str: Path to the YAML file.
    content: dict: Content to write to the YAML file.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as yaml_file:
            yaml.safe_dump(content, yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)   

def save_numpy_array_data(file_path:str, array:np.array)->None:
    """
    Save numpy array data to file
    file_path: str: File path to save the numpy array
    array: np.array: Numpy array data to be saved
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)   
    
def save_object(file_path:str, obj:object)->None:
    """
    Save a Python object to a file using dill
    file_path: str: File path to save the object
    obj: object: Python object to be saved
    """
    try:
        logging.info(f"Enter the save_object method of main_utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
        logging.info(f"Exit the save_object method of main_utils")
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def load_object(file_path:str)->object:
    """
    Load a Python object from a file using dill
    file_path: str: File path to load the object from
    return: object: Loaded Python object
    """
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        with open(file_path, 'rb') as file_obj:
            print(file_obj)
            return pickle.load(file_obj) 
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def load_numpy_array_data(file_path:str)->np.array:
    """
    Load numpy array data from file
    file_path: str: File path to load the numpy array from
    return: np.array: Loaded numpy array data
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def evaluate_models(x_train, y_train, x_test, y_test, models:dict, params:dict)->dict:
    """
    Evaluate multiple machine learning models and return their performance scores.
    """
    try:
        logging.info("Enter the evaluate_models method of main_utils")
        report = {}
        for model_name, model in models.items():
            param_grid = params.get(model_name, {})   # SAFE ACCESS
            if len(param_grid) > 0:
                gs = GridSearchCV(model, param_grid, cv=3)
                gs.fit(x_train, y_train)
                model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)
            train_model_score = r2_score(y_true=y_train, y_pred=y_train_pred)
            test_model_score = r2_score(y_true=y_test, y_pred=y_test_pred)
            report[model_name] = {
                "train_score": train_model_score,
                "test_score": test_model_score
            }
        logging.info("Exit the evaluate_models method of main_utils")
        return report
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
