import logging
from pathlib import Path

import click
import pandas as pd
from dotenv import find_dotenv, load_dotenv
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
def main(input_filepath, output_filepath):
    """Runs data processing scripts to turn raw data from (../raw) into
    cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info("training model")

    # Load data
    df = pd.read_csv(input_filepath)
    X = df.drop(['target', 'target_name'], axis=1)
    y = df['target']

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Log to MLflow
    mlruns_path = Path(output_filepath).parent / "mlruns"
    mlruns_path.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(str(mlruns_path))
    mlflow.set_experiment("iris_experiment")

    with mlflow.start_run():
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_param("random_state", 42)

        # Infer signature
        signature = infer_signature(X_train, model.predict(X_train))

        # Log model
        mlflow.sklearn.log_model(model, "model", signature=signature)

        logger.info(f"Model trained with accuracy: {accuracy}")

    # Save model locally
    import joblib
    joblib.dump(model, output_filepath)
    logger.info(f"Model saved to {output_filepath}")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
