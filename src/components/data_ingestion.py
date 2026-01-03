import os
import sys
import pandas as pd
from dataclasses import dataclass

from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import DataTransformation


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "raw.csv")


class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            logging.info("Starting data ingestion process")

            df = pd.read_csv("notebooks/data/dataset.csv")
            logging.info("Dataset loaded successfully")

            os.makedirs("artifacts", exist_ok=True)

            df.to_csv(self.data_ingestion_config.raw_data_path, index=False)
            logging.info("Raw data saved")

            train_set, test_set = train_test_split(
                df, test_size=0.2, random_state=42
            )

            train_set.to_csv(self.data_ingestion_config.train_data_path, index=False)
            test_set.to_csv(self.data_ingestion_config.test_data_path, index=False)

            logging.info("Train and test data saved successfully")
            logging.info("Data ingestion completed")

            return (
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()

    X_train_transformed, X_test_transformed, _ = (
        data_transformation.initiate_data_transformation(train_data, test_data)
    )
