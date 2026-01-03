import os
import sys
from dataclasses import dataclass

import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join(
        "artifacts", "preprocessor.pkl"
    )


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_transformer_object(self):
        """
        Creates and returns preprocessing pipeline
        """
        try:
            numerical_features = [
                "popularity", "duration_ms", "danceability", "energy",
                "loudness", "speechiness", "acousticness",
                "instrumentalness", "liveness", "valence",
                "tempo", "key", "mode", "time_signature"
            ]

            categorical_features = ["track_genre"]
            binary_features = ["explicit"]

            # Numerical pipeline
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            # Categorical pipeline
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore"))
                ]
            )

            logging.info("Numerical and categorical pipelines created")

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", num_pipeline, numerical_features),
                    ("cat", cat_pipeline, categorical_features),
                    ("bin", "passthrough", binary_features)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        """
        Reads data, applies preprocessing, saves preprocessor,
        and returns transformed data
        """
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Train and test data loaded successfully")

            # Drop unnecessary columns
            drop_columns = [
                "Unnamed: 0",
                "track_id",
                "track_name",
                "artists",
                "album_name"
            ]

            train_df.drop(columns=drop_columns, inplace=True, errors="ignore")
            test_df.drop(columns=drop_columns, inplace=True, errors="ignore")

            logging.info("Dropped unnecessary columns")

            preprocessor_obj = self.get_transformer_object()

            # ❌ No target column (content-based recommendation system)
            X_train = train_df
            X_test = test_df

            X_train_transformed = preprocessor_obj.fit_transform(X_train)
            X_test_transformed = preprocessor_obj.transform(X_test)

            logging.info("Data transformation completed")

            # Save preprocessor object
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )

            logging.info("Preprocessor object saved successfully")

            return (
                X_train_transformed,
                X_test_transformed,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)
