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