#!/usr/bin/env python3
"""ClearML Pipeline for Iris Classification

This script defines and executes a ClearML pipeline for the complete
ML workflow: data processing, model training, and evaluation.
"""

import logging
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from clearml import PipelineController, Task
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split


def data_processing_step(dataset_path: str, test_size: float = 0.2) -> dict[str, Any]:
    """Data processing pipeline step.

    Args:
        dataset_path: Path to the input dataset
        test_size: Fraction of data to use for testing

    Returns:
        Dictionary with processed data paths and metadata

    """
    task = Task.init(
        project_name="Iris Pipelines",
        task_name="data_processing",
        task_type=Task.TaskTypes.data_processing,
        reuse_last_task_id=False,
    )

    logger = logging.getLogger(__name__)
    logger.info("Starting data processing step")

    # Load data
    df = pd.read_csv(dataset_path)
    logger.info(f"Loaded dataset with shape: {df.shape}")

    # Basic data validation
    if "target" not in df.columns or "target_name" not in df.columns:
        raise ValueError("Dataset must contain 'target' and 'target_name' columns")

    # Split features and target
    X = df.drop(["target", "target_name"], axis=1)
    y = df["target"]
    target_names = df["target_name"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )

    logger.info(f"Train set: {X_train.shape}, Test set: {X_test.shape}")

    # Save processed data
    output_dir = Path("./pipeline_artifacts/data_processing")
    output_dir.mkdir(parents=True, exist_ok=True)

    train_data = pd.concat([X_train, y_train], axis=1)
    test_data = pd.concat([X_test, y_test], axis=1)

    train_path = output_dir / "train_data.csv"
    test_path = output_dir / "test_data.csv"

    train_data.to_csv(train_path, index=False)
    test_data.to_csv(test_path, index=False)

    # Log artifacts
    task.upload_artifact("train_data", train_data.head())
    task.upload_artifact("test_data", test_data.head())

    # Log dataset statistics
    dataset_stats = {
        "original_shape": df.shape,
        "train_shape": X_train.shape,
        "test_shape": X_test.shape,
        "n_features": X.shape[1],
        "n_classes": len(y.unique()),
        "class_distribution": y.value_counts().to_dict(),
        "feature_names": list(X.columns),
        "target_names": target_names.unique().tolist(),
    }

    task.upload_artifact("dataset_statistics", dataset_stats)

    # Log to ClearML logger
    from clearml import Logger

    clearml_logger = Logger.current_logger()
    clearml_logger.report_scalar("n_samples", "dataset", len(df), iteration=0)
    clearml_logger.report_scalar("n_features", "dataset", X.shape[1], iteration=0)
    clearml_logger.report_scalar("n_classes", "dataset", len(y.unique()), iteration=0)

    result = {
        "train_data_path": str(train_path),
        "test_data_path": str(test_path),
        "dataset_stats": dataset_stats,
        "feature_names": list(X.columns),
        "target_names": target_names.unique().tolist(),
    }

    task.close()
    return result


def model_training_step(
    train_data_path: str, model_type: str = "random_forest"
) -> dict[str, Any]:
    """Model training pipeline step.

    Args:
        train_data_path: Path to training data
        model_type: Type of model to train

    Returns:
        Dictionary with model information and metrics

    """
    task = Task.init(
        project_name="Iris Pipelines",
        task_name=f"train_{model_type}",
        task_type=Task.TaskTypes.training,
        reuse_last_task_id=False,
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Starting model training step: {model_type}")

    # Load training data
    train_df = pd.read_csv(train_data_path)
    X_train = train_df.drop("target", axis=1)
    y_train = train_df["target"]

    # Initialize model
    if model_type == "random_forest":
        from sklearn.ensemble import RandomForestClassifier

        model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        params = {"n_estimators": 100, "random_state": 42, "n_jobs": -1}
    elif model_type == "svm":
        from sklearn.svm import SVC

        model = SVC(random_state=42, probability=True)
        params = {"random_state": 42, "probability": True}
    elif model_type == "logistic_regression":
        from sklearn.linear_model import LogisticRegression

        model = LogisticRegression(random_state=42, max_iter=1000)
        params = {"random_state": 42, "max_iter": 1000}
    elif model_type == "gradient_boosting":
        from sklearn.ensemble import GradientBoostingClassifier

        model = GradientBoostingClassifier(random_state=42)
        params = {"random_state": 42}
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    # Log parameters
    task.connect(params, name="model_parameters")

    # Train model
    logger.info("Training model...")
    model.fit(X_train, y_train)

    # Calculate training metrics
    train_pred = model.predict(X_train)
    train_accuracy = accuracy_score(y_train, train_pred)

    logger.info(f"Training accuracy: {train_accuracy:.4f}")

    # Save model
    output_dir = Path("./pipeline_artifacts/model_training")
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / f"{model_type}_model.pkl"

    joblib.dump(model, model_path)

    # Log model to ClearML
    from clearml.model import Model

    clearml_model = Model.upload(
        model=model,
        name=f"iris_{model_type}_pipeline_model",
        project="Iris Pipelines",
        framework="sklearn",
        tags=["iris", "pipeline", model_type],
        comment=f"Training accuracy: {train_accuracy:.4f}",
    )

    # Log metrics and artifacts
    from clearml import Logger

    clearml_logger = Logger.current_logger()
    clearml_logger.report_scalar(
        "train_accuracy", "metrics", train_accuracy, iteration=0
    )

    # Log feature importance if available
    if hasattr(model, "feature_importances_"):
        feature_importance = dict(zip(X_train.columns, model.feature_importances_))
        clearml_logger.report_vector(
            "feature_importance",
            "features",
            values=list(feature_importance.values()),
            xaxis=list(feature_importance.keys()),
            iteration=0,
        )

    # Log classification report
    train_report = classification_report(y_train, train_pred, output_dict=True)
    task.upload_artifact("training_classification_report", train_report)

    result = {
        "model_path": str(model_path),
        "model_type": model_type,
        "train_accuracy": train_accuracy,
        "model_id": clearml_model.id,
        "feature_names": list(X_train.columns),
        "parameters": params,
    }

    task.close()
    return result


def model_evaluation_step(
    model_path: str, test_data_path: str, model_type: str
) -> dict[str, Any]:
    """Model evaluation pipeline step.

    Args:
        model_path: Path to trained model
        test_data_path: Path to test data
        model_type: Type of model

    Returns:
        Dictionary with evaluation metrics

    """
    task = Task.init(
        project_name="Iris Pipelines",
        task_name=f"evaluate_{model_type}",
        task_type=Task.TaskTypes.testing,
        reuse_last_task_id=False,
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Starting model evaluation step: {model_type}")

    # Load model and test data
    model = joblib.load(model_path)
    test_df = pd.read_csv(test_data_path)
    X_test = test_df.drop("target", axis=1)
    y_test = test_df["target"]

    # Make predictions
    y_pred = model.predict(X_test)
    y_pred_proba = (
        model.predict_proba(X_test) if hasattr(model, "predict_proba") else None
    )

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, output_dict=True)

    logger.info(f"Test accuracy: {accuracy:.4f}")

    # Log metrics
    from clearml import Logger

    clearml_logger = Logger.current_logger()
    clearml_logger.report_scalar("test_accuracy", "metrics", accuracy, iteration=0)

    # Log detailed classification metrics
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
    from sklearn.metrics import confusion_matrix

    conf_matrix = confusion_matrix(y_test, y_pred)
    clearml_logger.report_confusion_matrix(
        "confusion_matrix",
        "test",
        matrix=conf_matrix,
        iteration=0,
        xaxis="Predicted",
        yaxis="Actual",
    )

    # Create evaluation plots
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns

        # Confusion matrix plot
        plt.figure(figsize=(8, 6))
        target_names = ["setosa", "versicolor", "virginica"]  # Assuming Iris dataset
        sns.heatmap(
            conf_matrix,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=target_names,
            yticklabels=target_names,
        )
        plt.title(f"Confusion Matrix - {model_type}")
        plt.ylabel("Actual")
        plt.xlabel("Predicted")
        clearml_logger.report_matplotlib_figure(
            title="Confusion Matrix", series="plots", figure=plt, iteration=0
        )
        plt.close()

    except ImportError:
        logger.warning("matplotlib/seaborn not available for plotting")

    # Log artifacts
    task.upload_artifact("test_classification_report", class_report)
    task.upload_artifact("confusion_matrix", conf_matrix.tolist())

    evaluation_results = {
        "model_type": model_type,
        "test_accuracy": accuracy,
        "classification_report": class_report,
        "confusion_matrix": conf_matrix.tolist(),
        "n_test_samples": len(X_test),
    }

    task.upload_artifact("evaluation_results", evaluation_results)

    task.close()
    return evaluation_results


def create_pipeline(dataset_path: str, model_types: list = None) -> PipelineController:
    """Create and configure the ClearML pipeline.

    Args:
        dataset_path: Path to input dataset
        model_types: List of model types to train and evaluate

    Returns:
        Configured PipelineController

    """
    if model_types is None:
        model_types = ["random_forest"]

    # Create pipeline
    pipe = PipelineController(
        name="Iris Classification Pipeline", project="Iris Pipelines", version="1.0"
    )

    # Add data processing step
    pipe.add_function_step(
        name="data_processing",
        function=data_processing_step,
        function_kwargs={"dataset_path": dataset_path},
        function_return=["train_data_path", "test_data_path", "dataset_stats"],
    )

    # Add model training and evaluation steps for each model type
    for model_type in model_types:
        # Training step
        pipe.add_function_step(
            name=f"train_{model_type}",
            function=model_training_step,
            function_kwargs={
                "train_data_path": "${data_processing.train_data_path}",
                "model_type": model_type,
            },
            function_return=[f"{model_type}_results"],
            parents=["data_processing"],
        )

        # Evaluation step
        pipe.add_function_step(
            name=f"evaluate_{model_type}",
            function=model_evaluation_step,
            function_kwargs={
                "model_path": f"${{train_{model_type}.{model_type}_results.model_path}}",
                "test_data_path": "${data_processing.test_data_path}",
                "model_type": model_type,
            },
            function_return=[f"{model_type}_evaluation"],
            parents=[f"train_{model_type}"],
        )

    return pipe


def run_pipeline(dataset_path: str, model_types: list = None, execute: bool = True):
    """Run the ClearML pipeline.

    Args:
        dataset_path: Path to input dataset
        model_types: List of model types to train
        execute: Whether to execute the pipeline immediately

    """
    if model_types is None:
        model_types = ["random_forest"]

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Creating pipeline for models: {model_types}")

    # Create pipeline
    pipe = create_pipeline(dataset_path, model_types)

    if execute:
        logger.info("Executing pipeline...")
        # Execute pipeline
        pipe.start_locally()

        logger.info("Pipeline execution completed")
        logger.info(f"Pipeline ID: {pipe.pipeline_id}")

        return pipe.pipeline_id
    else:
        logger.info("Pipeline created but not executed")
        return pipe


def main():
    """Main function to run the pipeline."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run ClearML pipeline for Iris classification"
    )
    parser.add_argument("--dataset", required=True, help="Path to input dataset")
    parser.add_argument(
        "--models",
        nargs="+",
        default=["random_forest"],
        choices=["random_forest", "svm", "logistic_regression", "gradient_boosting"],
        help="Model types to train and evaluate",
    )
    parser.add_argument(
        "--no-execute", action="store_true", help="Create pipeline but do not execute"
    )

    args = parser.parse_args()

    # Ensure output directories exist
    Path("./pipeline_artifacts").mkdir(parents=True, exist_ok=True)

    # Run pipeline
    pipeline_id = run_pipeline(
        dataset_path=args.dataset, model_types=args.models, execute=not args.no_execute
    )

    if pipeline_id:
        print(f"Pipeline completed. ID: {pipeline_id}")


if __name__ == "__main__":
    main()
