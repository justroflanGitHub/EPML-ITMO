#!/usr/bin/env python3
"""Evaluate trained model on test data."""

import json
import pickle
import sys
from pathlib import Path

import pandas as pd
import yaml
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


def main():
    if len(sys.argv) != 6:
        print(
            "Usage: python evaluate_model.py <dataset> <algorithm> <model_file> <test_file> <config_file>"
        )
        return 1

    dataset = sys.argv[1]
    algorithm = sys.argv[2]
    model_file = sys.argv[3]
    test_file = sys.argv[4]
    config_file = sys.argv[5]

    try:
        # Load configuration
        with open(config_file) as f:
            config = yaml.safe_load(f)

        # Load test data
        test_df = pd.read_csv(test_file)
        X_test = test_df.drop("target", axis=1)
        y_test = test_df["target"]

        # Load model
        with open(model_file, "rb") as f:
            model = pickle.load(f)

        # Make predictions
        y_pred = model.predict(X_test)

        # Calculate metrics
        metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision_macro": float(precision_score(y_test, y_pred, average="macro")),
            "precision_micro": float(precision_score(y_test, y_pred, average="micro")),
            "recall_macro": float(recall_score(y_test, y_pred, average="macro")),
            "recall_micro": float(recall_score(y_test, y_pred, average="micro")),
            "f1_macro": float(f1_score(y_test, y_pred, average="macro")),
            "f1_micro": float(f1_score(y_test, y_pred, average="micro")),
        }

        # Create predictions dataframe
        predictions_df = pd.DataFrame(
            {
                "true_label": y_test,
                "predicted_label": y_pred,
                "correct": (y_test == y_pred).astype(int),
            }
        )

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        cm_df = pd.DataFrame(cm)

        # Classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose()

        # Ensure output directory exists
        base_dir = f"reports/{dataset}/{algorithm}"
        Path(base_dir).mkdir(parents=True, exist_ok=True)

        # Save results
        with open(f"{base_dir}/metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)

        predictions_df.to_csv(f"{base_dir}/predictions.csv", index=False)
        cm_df.to_csv(f"{base_dir}/confusion_matrix.csv", index=False)
        report_df.to_csv(f"{base_dir}/classification_report.csv", index=True)

        print(f"Evaluation completed for {algorithm} on {dataset}")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        return 0

    except Exception as e:
        print(f"Error evaluating model: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
