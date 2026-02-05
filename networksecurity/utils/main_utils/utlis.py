import pickle
import yaml # used for reading yaml files
import dill # used for piclking the files
import numpy as np
import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

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