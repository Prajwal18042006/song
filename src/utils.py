import os
import sys
import joblib
from src.exception import CustomException
from src.logger import logging


def save_object(file_path, obj):
    """
    Saves any Python object using joblib
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        joblib.dump(obj, file_path)

        logging.info(f"Object saved successfully at {file_path}")

    except Exception as e:
        raise CustomException(e, sys)
def load_object(file_path):
    try:
        with open(file_path, "rb") as file:
            return joblib.load(file)
    except Exception as e:
        raise CustomException(e, sys)
