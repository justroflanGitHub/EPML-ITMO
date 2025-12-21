#!/usr/bin/env python3
"""Perform cross-validation evaluation."""

import json
import sys
from pathlib import Path

import pandas as pd
import yaml
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
)
from sklearn.model_selection import cross_validate
from sklearn.svm import SVC


def main():
    if len(sys.argv) != 5:
        print(
            "Usage: python cross_validation.py <dataset> <algorithm> <train_file> <config_file>"
        )
        return 1

    dataset = sys.argv[1]
    algorithm = sys.argv[2]
    train_file = sys.argv[3]
    config_file = sys.argv[4]

    try:
        # Load configuration
        with open(config_file) as f:
            config = yaml.safe_load(f)

        # Load training data
        train_file = f"data/processed/{dataset}/train.csv"
        train_df = pd.read_csv(train_file)
        X = train_df.drop("target", axis=1)
        y = train_df["target"]

        hyperparameters = config["model"]["hyperparameters"]

        # Initialize model
        if algorithm == "random_forest":
            model = RandomForestClassifier(**hyperparameters)
        elif algorithm == "svm":
            model = SVC(**hyperparameters)
        elif algorithm == "logistic_regression":
            model = LogisticRegression(**hyperparameters)
        elif algorithm == "gradient_boosting":
            model = GradientBoostingClassifier(**hyperparameters)

        # Define scorers
        scorers = {
            "accuracy": make_scorer(accuracy_score),
            "precision_macro": make_scorer(precision_score, average="macro"),
            "recall_macro": make_scorer(recall_score, average="macro"),
            "f1_macro": make_scorer(f1_score, average="macro"),
        }

        # Perform cross-validation
        cv_results = cross_validate(
            model,
            X,
            y,
            scoring=scorers,
            cv=config.get("evaluation", {}).get("cv_folds", 5),
            return_train_score=False,
        )

        # Prepare results
        results = {
            "algorithm": algorithm,
            "dataset": dataset,
            "cv_folds": config.get("evaluation", {}).get("cv_folds", 5),
            "scores": {},
        }

        for scorer_name in scorers.keys():
            results["scores"][scorer_name] = {
                "mean": float(cv_results[f"test_{scorer_name}"].mean()),
                "std": float(cv_results[f"test_{scorer_name}"].std()),
                "values": cv_results[f"test_{scorer_name}"].tolist(),
            }

        # Summary statistics
        summary = {
            "best_metric": "accuracy",
            "best_score": results["scores"]["accuracy"]["mean"],
            "cv_std": results["scores"]["accuracy"]["std"],
            "all_metrics": list(results["scores"].keys()),
        }

        # Ensure output directory exists
        base_dir = f"reports/{dataset}/{algorithm}"
        Path(base_dir).mkdir(parents=True, exist_ok=True)

        # Save results
        with open(f"{base_dir}/cv_results.json", "w") as f:
            json.dump(results, f, indent=2)

        with open(f"{base_dir}/cv_summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        print(f"Cross-validation completed for {algorithm} on {dataset}")
        print(
            f"Mean CV accuracy: {results['scores']['accuracy']['mean']:.4f} ± {results['scores']['accuracy']['std']:.4f}"
        )
        return 0

    except Exception as e:
        print(f"Error performing cross-validation: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
