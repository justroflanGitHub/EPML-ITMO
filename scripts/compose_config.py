#!/usr/bin/env python3
"""Compose configuration for specific algorithm and dataset."""

import os
import sys

import yaml


def main():
    if len(sys.argv) != 3:
        print("Usage: python compose_config.py <dataset> <algorithm>")
        return 1

    dataset = sys.argv[1]
    algorithm = sys.argv[2]

    try:
        # Create composed configuration with resolved values
        config = {
            "seed": 42,
            "experiment_name": "ml_pipeline_experiment",
            "output_dir": "outputs/ml_pipeline_experiment",
            "log_level": "INFO",
            "data": {
                "name": dataset,
                "test_size": 0.2,
                "validation_size": 0.2,
                "random_state": 42,
            },
            "model": {"algorithm": algorithm},
            "training": {
                "epochs": 100,
                "batch_size": 32,
                "learning_rate": 0.001,
                "early_stopping": True,
                "patience": 10,
                "validation_metric": "accuracy",
                "optimizer": "adam",
                "loss_function": "cross_entropy",
            },
            "evaluation": {
                "metrics": ["accuracy", "precision_macro", "recall_macro", "f1_macro"],
                "cross_validation": True,
                "cv_folds": 5,
                "save_confusion_matrix": True,
                "save_classification_report": True,
                "plot_roc_curve": False,
                "plot_precision_recall_curve": False,
            },
        }

        # Load dataset-specific configuration
        dataset_config_file = f"config/hydra/data/{dataset}.yaml"
        if os.path.exists(dataset_config_file):
            with open(dataset_config_file) as f:
                dataset_config = yaml.safe_load(f)
            # Merge dataset config, but override with resolved values
            for key, value in dataset_config.items():
                if key == "random_state" and isinstance(value, str) and "${" in value:
                    config["data"][key] = 42
                else:
                    config["data"][key] = value

        # Load model-specific configuration
        model_config_file = f"config/hydra/model/{algorithm}.yaml"
        if os.path.exists(model_config_file):
            with open(model_config_file) as f:
                model_config = yaml.safe_load(f)
            # Merge model config properly
            config["model"] = model_config

        # Save composed configuration
        output_file = f"config/composed/{dataset}_{algorithm}.yaml"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, "w") as f:
            yaml.dump(config, f, default_flow_style=False)

        print(f"Composed configuration saved to {output_file}")
        return 0

    except Exception as e:
        print(f"Configuration composition failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
