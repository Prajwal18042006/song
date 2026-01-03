import os
import sys
import numpy as np
import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src.utils import load_object


class PredictionPipeline:
    def __init__(self):
        self.preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")
        self.model_path = os.path.join("artifacts", "knn_model.pkl")
        self.data_path = os.path.join("artifacts", "raw.csv")

    def recommend_songs(self, song_name, n_recommendations=5):
        """
        Recommend top-N similar songs based on song name
        """
        try:
            logging.info("Starting prediction pipeline")

            # Load objects
            preprocessor = load_object(self.preprocessor_path)
            knn_model = load_object(self.model_path)

            # Load raw dataset
            df = pd.read_csv(self.data_path)

            # Case-insensitive song matching
            song_name_lower = song_name.lower().strip()
            df["track_name_lower"] = df["track_name"].str.lower().str.strip()
            
            # Check if song exists (case-insensitive)
            matching_songs = df[df["track_name_lower"] == song_name_lower]
            
            if matching_songs.empty:
                # Try partial match
                partial_matches = df[df["track_name_lower"].str.contains(song_name_lower, na=False)]
                if not partial_matches.empty:
                    # Use first partial match
                    song_index = partial_matches.index[0]
                    logging.info(f"Using partial match: {df.loc[song_index, 'track_name']}")
                else:
                    # Show some suggestions
                    suggestions = df["track_name"].head(10).tolist()
                    raise ValueError(
                        f"Song '{song_name}' not found in dataset. "
                        f"Here are some sample songs: {', '.join(suggestions[:5])}"
                    )
            else:
                # Use first exact match
                song_index = matching_songs.index[0]
            
            # Drop the temporary column
            df = df.drop(columns=["track_name_lower"], errors="ignore")

            # Drop non-feature columns
            drop_columns = [
                "Unnamed: 0",
                "track_id",
                "track_name",
                "artists",
                "album_name"
            ]

            X = df.drop(columns=drop_columns, errors="ignore")

            # Transform data
            X_transformed = preprocessor.transform(X)

            # Find nearest neighbors
            distances, indices = knn_model.kneighbors(
                X_transformed[song_index].reshape(1, -1),
                n_neighbors=n_recommendations + 1
            )

            # Remove the input song itself
            recommended_indices = indices[0][1:]

            recommendations = df.iloc[recommended_indices][
                ["track_name", "artists", "track_genre", "popularity"]
            ]

            logging.info("Recommendations generated successfully")

            return recommendations

        except Exception as e:
            raise CustomException(e, sys)
