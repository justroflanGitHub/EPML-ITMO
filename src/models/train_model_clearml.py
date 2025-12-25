#!/usr/bin/env python3
"""Train Model with ClearML Integration.

This script trains a machine learning model and logs experiments to ClearML.
It provides comprehensive experiment tracking, model versioning, and metadata logging.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

import click
import joblib
import pandas as pd
import yaml

# ClearML imports - handle missing credentials gracefully
try:
    from clearml import Logger, Task
    from clearml.model import Model

    CLEARML_AVAILABLE = True
    # Check if credentials are configured
    if not (
        os.getenv("CLEARML_API_ACCESS_KEY") and os.getenv("CLEARML_API_SECRET_KEY")
    ):
        CLEARML_AVAILABLE = False
        print("⚠ ClearML credentials not found - running in demo mode")
except ImportError:
    CLEARML_AVAILABLE = False
    print("⚠ ClearML not available - running in demo mode")

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


@click.command()
@click.argument("input_filepath", type=click.Path(exists=True))
@click.argument("output_filepath", type=click.Path())
@click.option("--model-type", default="random_forest", help="Type of model to train")
@click.option("--experiment-name", default=None, help="ClearML experiment name")
@click.option(
    "--project-name", default="Iris Data Science Project", help="ClearML project name"
)
@click.option("--demo-mode", is_flag=True, help="Run in demo mode without ClearML")
def main(
    input_filepath,
    output_filepath,
    model_type,
    experiment_name,
    project_name,
    demo_mode,
):
    """Train a machine learning model with ClearML experiment tracking."""
    logger = logging.getLogger(__name__)

    # Determine if we should use ClearML
    use_clearml = CLEARML_AVAILABLE and not demo_mode

    # Generate experiment name if not provided
    if experiment_name is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        experiment_name = f"iris_{model_type}_{timestamp}"

    if use_clearml:
        logger.info(f"Training {model_type} model with ClearML tracking")
        logger.info(f"Experiment: {experiment_name}")
        logger.info(f"Project: {project_name}")

        # Initialize ClearML Task
        task = Task.init(
            project_name=project_name,
            task_name=experiment_name,
            task_type=Task.TaskTypes.training,
            reuse_last_task_id=False,
        )
        clearml_logger = Logger.current_logger()
        task.set_system_tags(["iris", "classification", "mlops"])
    else:
        logger.info(f"Training {model_type} model (demo mode)")
        logger.info(f"Experiment: {experiment_name}")
        task = None
        clearml_logger = None

    # Load configuration
    config_path = (
        Path(__file__).resolve().parents[2] / "config" / "clearml" / "config.yaml"
    )
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
        if use_clearml:
            # Log configuration
            task.connect(config, name="clearml_config")
        logger.info("ClearML configuration loaded")

    # Log parameters
    if use_clearml:
        task.connect(
            {
                "model_type": model_type,
                "input_filepath": input_filepath,
                "output_filepath": output_filepath,
                "experiment_name": experiment_name,
                "project_name": project_name,
            },
            name="script_parameters",
        )

    # Load and prepare data
    logger.info(f"Loading data from {input_filepath}")
    df = pd.read_csv(input_filepath)

    # Log dataset information
    dataset_info = {
        "shape": df.shape,
        "columns": list(df.columns),
        "target_classes": (
            df["target_name"].unique().tolist() if "target_name" in df.columns else None
        ),
    }

    if use_clearml:
        task.upload_artifact("dataset_info", dataset_info)

    # Prepare features and target
    columns_to_drop = ["target"]
    if "target_name" in df.columns:
        columns_to_drop.append("target_name")
    X = df.drop(columns_to_drop, axis=1)
    y = df["target"]

    # Log feature information
    feature_info = {
        "n_features": X.shape[1],
        "feature_names": list(X.columns),
        "target_distribution": y.value_counts().to_dict(),
    }

    if use_clearml:
        task.upload_artifact("feature_info", feature_info)

    # Split data
    test_size = 0.2
    random_state = 42
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    logger.info(f"Train set: {X_train.shape}, Test set: {X_test.shape}")

    # Initialize model based on type
    if model_type == "random_forest":
        model = RandomForestClassifier(
            n_estimators=100, random_state=random_state, n_jobs=-1
        )
        model_params = {"n_estimators": 100, "random_state": random_state, "n_jobs": -1}
    elif model_type == "svm":
        from sklearn.svm import SVC

        model = SVC(random_state=random_state, probability=True)
        model_params = {"random_state": random_state, "probability": True}
    elif model_type == "logistic_regression":
        from sklearn.linear_model import LogisticRegression

        model = LogisticRegression(random_state=random_state, max_iter=1000)
        model_params = {"random_state": random_state, "max_iter": 1000}
    elif model_type == "gradient_boosting":
        from sklearn.ensemble import GradientBoostingClassifier

        model = GradientBoostingClassifier(random_state=random_state)
        model_params = {"random_state": random_state}
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    # Log model parameters
    if use_clearml:
        task.connect(model_params, name="model_hyperparameters")

    # Train model
    logger.info("Training model...")
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = (
        model.predict_proba(X_test) if hasattr(model, "predict_proba") else None
    )

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, output_dict=True)
    conf_matrix = confusion_matrix(y_test, y_pred)

    logger.info(f"Model accuracy: {accuracy:.4f}")

    # Log metrics to ClearML
    if use_clearml:
        clearml_logger.report_scalar("accuracy", "test", accuracy, iteration=0)

        # Log classification report metrics
        for class_name, metrics in class_report.items():
            if isinstance(metrics, dict):
                for metric_name, value in metrics.items():
                    if isinstance(value, (int, float)):
                        clearml_logger.report_scalar(
                            f"{class_name}_{metric_name}",
                            "classification_report",
                            value,
                            iteration=0,
                        )

        # Log confusion matrix
        clearml_logger.report_confusion_matrix(
            "confusion_matrix",
            "test",
            matrix=conf_matrix,
            iteration=0,
            xaxis="Predicted",
            yaxis="Actual",
        )

        # Log feature importance if available
        if hasattr(model, "feature_importances_"):
            feature_importance = dict(zip(X.columns, model.feature_importances_))
            clearml_logger.report_vector(
                "feature_importance",
                "features",
                values=list(feature_importance.values()),
                xaxis=list(feature_importance.keys()),
                iteration=0,
            )

    # Log plots
    if use_clearml:
        try:
            import matplotlib.pyplot as plt
            import seaborn as sns

            # Confusion matrix plot
            plt.figure(figsize=(8, 6))
            target_labels = (
                df["target_name"].unique()
                if "target_name" in df.columns
                else [f"Class {i}" for i in range(len(conf_matrix))]
            )
            sns.heatmap(
                conf_matrix,
                annot=True,
                fmt="d",
                cmap="Blues",
                xticklabels=target_labels,
                yticklabels=target_labels,
            )
            plt.title("Confusion Matrix")
            plt.ylabel("Actual")
            plt.xlabel("Predicted")
            clearml_logger.report_matplotlib_figure(
                title="Confusion Matrix", series="plots", figure=plt, iteration=0
            )
            plt.close()

            # Feature importance plot (if available)
            if hasattr(model, "feature_importances_"):
                plt.figure(figsize=(10, 6))
                importance_df = pd.DataFrame(
                    {"feature": X.columns, "importance": model.feature_importances_}
                ).sort_values("importance", ascending=True)

                plt.barh(importance_df["feature"], importance_df["importance"])
                plt.title("Feature Importance")
                plt.xlabel("Importance")
                plt.tight_layout()
                clearml_logger.report_matplotlib_figure(
                    title="Feature Importance", series="plots", figure=plt, iteration=0
                )
                plt.close()

        except ImportError:
            logger.warning("matplotlib/seaborn not available for plotting")

    # Create and log model artifact
    model_path = Path(output_filepath)
    model_path.parent.mkdir(parents=True, exist_ok=True)

    # Save model locally
    joblib.dump(model, output_filepath)
    logger.info(f"Model saved to {output_filepath}")

    # Log model to ClearML
    if use_clearml:
        clearml_model = Model.upload(
            model=model,
            name=f"iris_{model_type}_model",
            project=project_name,
            framework="sklearn",
            tags=["iris", "classification", model_type],
            comment=f"Accuracy: {accuracy:.4f}",
        )

        # Connect model to task
        task.connect(clearml_model, name="output_model")

        # Log additional artifacts
        task.upload_artifact("classification_report", class_report)
        task.upload_artifact("confusion_matrix", conf_matrix.tolist())
        task.upload_artifact(
            "model_metadata",
            {
                "model_type": model_type,
                "accuracy": accuracy,
                "n_features": X.shape[1],
                "n_classes": len(y.unique()),
                "training_samples": len(X_train),
                "test_samples": len(X_test),
                "created_at": datetime.now().isoformat(),
            },
        )

        logger.info("✓ Model training completed with ClearML tracking")
        logger.info(f"✓ Accuracy: {accuracy:.4f}")
        logger.info(f"✓ ClearML Task: {task.id}")

        # Close the task
        task.close()
    else:
        logger.info("✓ Model training completed (demo mode)")
        logger.info(f"✓ Accuracy: {accuracy:.4f}")
        logger.info("✓ Model saved locally (ClearML logging disabled)")

    return accuracy


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()
