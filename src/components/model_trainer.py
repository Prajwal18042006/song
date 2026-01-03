import os
import sys
from dataclasses import dataclass

from sklearn.neighbors import NearestNeighbors

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class ModelTrainerConfig:
    knn_model_path = os.path.join(
        "artifacts", "knn_model.pkl"
    )


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, X_train_transformed, n_neighbors=10):
        """
        Trains KNN model using cosine distance
        """
        try:
            logging.info("Starting KNN-based model trainer")

            knn_model = NearestNeighbors(
                n_neighbors=n_neighbors,
                metric="cosine",
                algorithm="brute"
            )

            knn_model.fit(X_train_transformed)

            logging.info("KNN model trained successfully")

            save_object(
                file_path=self.model_trainer_config.knn_model_path,
                obj=knn_model
            )

            logging.info("KNN model saved successfully")

            return self.model_trainer_config.knn_model_path

        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    import numpy as np

    dummy_data = np.random.rand(10, 5)

    model_trainer = ModelTrainer()
    model_trainer.initiate_model_trainer(dummy_data)
