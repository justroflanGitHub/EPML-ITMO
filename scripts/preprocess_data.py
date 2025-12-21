#!/usr/bin/env python3
"""Preprocess data and create train/test splits."""

import json
import sys
from pathlib import Path

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split


def main():
    if len(sys.argv) != 4:
        print("Usage: python preprocess_data.py <dataset> <algorithm> <config_file>")
        return 1

    dataset = sys.argv[1]
    algorithm = sys.argv[2]
    config_file = sys.argv[3]

    try:
        # Load configuration
        with open(config_file) as f:
            config = yaml.safe_load(f)

        # Load raw data
        raw_file = f"data/raw/{dataset}.csv"
        df = pd.read_csv(raw_file)

        # Prepare features and target
        if dataset == "iris":
            X = df.drop(["target", "target_name"], axis=1)
            y = df["target"]
            feature_names = list(X.columns)
            target_names = df["target_name"].unique().tolist()

        # Split data
        test_size = config.get("data", {}).get("test_size", 0.2)
        random_state = config.get("seed", 42)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )

        # Combine back into dataframes
        train_df = pd.concat([X_train, y_train], axis=1)
        test_df = pd.concat([X_test, y_test], axis=1)

        # Ensure output directories exist
        train_file = f"data/processed/{dataset}/train.csv"
        test_file = f"data/processed/{dataset}/test.csv"
        metadata_file = f"data/processed/{dataset}/metadata.json"

        Path(train_file).parent.mkdir(parents=True, exist_ok=True)

        # Save processed data
        train_df.to_csv(train_file, index=False)
        test_df.to_csv(test_file, index=False)

        # Save metadata
        metadata = {
            "dataset": dataset,
            "algorithm": algorithm,
            "n_features": len(feature_names),
            "n_classes": len(target_names),
            "feature_names": feature_names,
            "target_names": target_names,
            "train_samples": len(train_df),
            "test_samples": len(test_df),
            "test_size": test_size,
            "random_state": random_state,
        }

        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"Preprocessed data saved for {dataset} dataset")
        return 0

    except Exception as e:
        print(f"Error preprocessing data: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
