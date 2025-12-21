#!/usr/bin/env python3
"""Train a model with specified algorithm."""

import json
import logging
import pickle
import sys
from pathlib import Path

import pandas as pd
import yaml
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC


def main():
    if len(sys.argv) != 4:
        print("Usage: python train_model.py <dataset> <algorithm> <config_file>")
        return 1

    dataset = sys.argv[1]
    algorithm = sys.argv[2]
    config_file = sys.argv[3]

    try:
        # Setup logging
        log_file = f"models/{dataset}/{algorithm}/training.log"
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        logger = logging.getLogger(__name__)

        # Load configuration
        with open(config_file) as f:
            config = yaml.safe_load(f)

        # Load training data
        train_file = f"data/processed/{dataset}/train.csv"
        train_df = pd.read_csv(train_file)
        X_train = train_df.drop("target", axis=1)
        y_train = train_df["target"]

        hyperparameters = config["model"]["hyperparameters"]

        logger.info(f"Starting training for {algorithm} on {dataset} dataset")
        logger.info(f"Hyperparameters: {hyperparameters}")

        # Initialize model based on algorithm
        if algorithm == "random_forest":
            model = RandomForestClassifier(**hyperparameters)
        elif algorithm == "svm":
            model = SVC(**hyperparameters)
        elif algorithm == "logistic_regression":
            model = LogisticRegression(**hyperparameters)
        elif algorithm == "gradient_boosting":
            model = GradientBoostingClassifier(**hyperparameters)
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        # Train model
        model.fit(X_train, y_train)

        # Save model
        model_file = f"models/{dataset}/{algorithm}/model.pkl"
        with open(model_file, "wb") as f:
            pickle.dump(model, f)

        # Save parameters
        params_file = f"models/{dataset}/{algorithm}/params.json"
        params_info = {
            "algorithm": algorithm,
            "dataset": dataset,
            "hyperparameters": hyperparameters,
            "n_features": X_train.shape[1],
            "n_samples": len(X_train),
            "model_type": str(type(model).__name__),
        }

        with open(params_file, "w") as f:
            json.dump(params_info, f, indent=2)

        logger.info(f"Model {algorithm} trained and saved successfully")
        print(f"Model {algorithm} trained successfully")
        return 0

    except Exception as e:
        print(f"Error training model: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
