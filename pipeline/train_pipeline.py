from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

if __name__ == "__main__":

    # Data ingestion
    ingestion = DataIngestion()
    train_path, test_path = ingestion.initiate_data_ingestion()

    # Data transformation
    transformation = DataTransformation()
    X_train_transformed, X_test_transformed, _ = transformation.initiate_data_transformation(
        train_path, test_path
    )

    # Model training (cosine similarity)
    model_trainer = ModelTrainer()
    model_trainer.initiate_model_trainer(X_train_transformed, n_neighbors=10)

