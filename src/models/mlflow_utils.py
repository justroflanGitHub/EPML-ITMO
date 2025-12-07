"""MLflow utilities for experiment tracking and model management.

This module provides decorators, context managers, and utility functions
for comprehensive MLflow experiment tracking.
"""

import functools
import logging
import time
from collections.abc import Callable
from contextlib import contextmanager
from typing import Any

import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.models import infer_signature
from sklearn.base import BaseEstimator
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

logger = logging.getLogger(__name__)


def setup_mlflow_tracking(
    tracking_uri: str | None = None,
    experiment_name: str = "iris_experiment",
    backend_store_uri: str | None = None,
    artifact_store_uri: str | None = None,
) -> None:
    """Set up MLflow tracking with database backend and artifact store.

    Args:
        tracking_uri: URI for MLflow tracking server
        experiment_name: Name of the experiment
        backend_store_uri: URI for backend store (database)
        artifact_store_uri: URI for artifact store

    """
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)

    if backend_store_uri:
        mlflow.set_backend_store_uri(backend_store_uri)

    if artifact_store_uri:
        mlflow.set_artifact_store_uri(artifact_store_uri)

    # Create experiment if it doesn't exist
    try:
        mlflow.create_experiment(experiment_name)
    except mlflow.exceptions.MlflowException:
        logger.info(f"Experiment '{experiment_name}' already exists")

    mlflow.set_experiment(experiment_name)
    logger.info(f"MLflow tracking set up for experiment: {experiment_name}")


@contextmanager
def mlflow_run_context(run_name: str | None = None, tags: dict[str, Any] | None = None):
    """Context manager for MLflow runs.

    Args:
        run_name: Name for the run
        tags: Dictionary of tags to set for the run

    """
    with mlflow.start_run(run_name=run_name) as run:
        if tags:
            for key, value in tags.items():
                mlflow.set_tag(key, value)

        logger.info(f"Started MLflow run: {run.info.run_id}")
        try:
            yield run
        finally:
            logger.info(f"Completed MLflow run: {run.info.run_id}")


def log_model_info(model: BaseEstimator, model_name: str = "model") -> None:
    """Log comprehensive model information to MLflow.

    Args:
        model: Trained sklearn model
        model_name: Name for the model artifact

    """
    # Log model parameters
    if hasattr(model, "get_params"):
        params = model.get_params()
        for param_name, param_value in params.items():
            mlflow.log_param(param_name, param_value)

    # Log model type and class
    mlflow.set_tag("model_type", type(model).__name__)
    mlflow.set_tag("model_module", type(model).__module__)


def log_metrics_dict(metrics: dict[str, float]) -> None:
    """Log a dictionary of metrics to MLflow.

    Args:
        metrics: Dictionary of metric names and values

    """
    for metric_name, metric_value in metrics.items():
        mlflow.log_metric(metric_name, metric_value)


def log_classification_metrics(
    y_true: pd.Series, y_pred: pd.Series, prefix: str = ""
) -> dict[str, float]:
    """Calculate and log comprehensive classification metrics.

    Args:
        y_true: True labels
        y_pred: Predicted labels
        prefix: Prefix for metric names

    Returns:
        Dictionary of calculated metrics

    """
    metrics = {}

    # Basic metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average="weighted")
    recall = recall_score(y_true, y_pred, average="weighted")
    f1 = f1_score(y_true, y_pred, average="weighted")

    metrics[f"{prefix}accuracy"] = accuracy
    metrics[f"{prefix}precision"] = precision
    metrics[f"{prefix}recall"] = recall
    metrics[f"{prefix}f1_score"] = f1

    # Log to MLflow
    log_metrics_dict(metrics)

    # Log detailed classification report as artifact
    report = classification_report(y_true, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    report_path = "classification_report.csv"
    report_df.to_csv(report_path)
    mlflow.log_artifact(report_path)

    # Log confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    cm_df = pd.DataFrame(cm)
    cm_path = "confusion_matrix.csv"
    cm_df.to_csv(cm_path, index=False)
    mlflow.log_artifact(cm_path)

    return metrics


def mlflow_experiment_tracker(
    experiment_name: str | None = None,
    log_model: bool = True,
    log_signature: bool = True,
    tags: dict[str, Any] | None = None,
):
    """Decorator for automatic MLflow experiment tracking.

    Args:
        experiment_name: Name of the experiment
        log_model: Whether to log the model
        log_signature: Whether to log model signature
        tags: Tags to set for the run

    """

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Set experiment if specified
            if experiment_name:
                mlflow.set_experiment(experiment_name)

            with mlflow_run_context(tags=tags) as run:
                start_time = time.time()

                try:
                    # Call the original function
                    result = func(*args, **kwargs)

                    # Log execution time
                    execution_time = time.time() - start_time
                    mlflow.log_metric("execution_time", execution_time)

                    # If result contains model and data, log them
                    if isinstance(result, dict):
                        model = result.get("model")
                        X_train = result.get("X_train")
                        y_pred = result.get("y_pred")
                        y_true = result.get("y_true")

                        if model and log_model:
                            if log_signature and X_train is not None:
                                signature = infer_signature(
                                    X_train, model.predict(X_train)
                                )
                                mlflow.sklearn.log_model(
                                    model, "model", signature=signature
                                )
                            else:
                                mlflow.sklearn.log_model(model, "model")

                        if y_pred is not None and y_true is not None:
                            log_classification_metrics(y_true, y_pred)

                    return result

                except Exception as e:
                    mlflow.set_tag("status", "failed")
                    mlflow.set_tag("error", str(e))
                    logger.error(f"Experiment failed: {e}")
                    raise

        return wrapper

    return decorator


class ExperimentManager:
    """Manager class for MLflow experiments with comparison capabilities."""

    def __init__(self, experiment_name: str = "iris_experiment"):
        self.experiment_name = experiment_name
        mlflow.set_experiment(experiment_name)

    def get_experiment_runs(self, filter_string: str = "") -> pd.DataFrame:
        """Get all runs for the experiment with optional filtering.

        Args:
            filter_string: MLflow filter string

        Returns:
            DataFrame with run information

        """
        runs = mlflow.search_runs(
            experiment_names=[self.experiment_name],
            filter_string=filter_string,
            order_by=["metrics.accuracy DESC"],
        )
        return runs

    def compare_runs(self, run_ids: list) -> pd.DataFrame:
        """Compare specific runs by their IDs.

        Args:
            run_ids: List of run IDs to compare

        Returns:
            DataFrame with comparison data

        """
        filter_string = " OR ".join([f"run_id = '{rid}'" for rid in run_ids])
        return self.get_experiment_runs(filter_string)

    def get_best_run(self, metric: str = "accuracy", mode: str = "max") -> pd.DataFrame:
        """Get the best run based on a metric.

        Args:
            metric: Metric to optimize
            mode: "max" or "min"

        Returns:
            DataFrame with best run

        """
        order_by = [f"metrics.{metric} {'DESC' if mode == 'max' else 'ASC'}"]
        runs = mlflow.search_runs(
            experiment_names=[self.experiment_name], order_by=order_by, max_results=1
        )
        return runs

    def log_run_summary(self, run_id: str) -> dict[str, Any]:
        """Get comprehensive summary of a run.

        Args:
            run_id: Run ID to summarize

        Returns:
            Dictionary with run summary

        """
        run = mlflow.get_run(run_id)

        summary = {
            "run_id": run_id,
            "status": run.info.status,
            "start_time": run.info.start_time,
            "end_time": run.info.end_time,
            "parameters": run.data.params,
            "metrics": run.data.metrics,
            "tags": run.data.tags,
        }

        return summary


def create_experiment_comparison_report(experiment_manager: ExperimentManager) -> str:
    """Create a markdown report comparing experiments.

    Args:
        experiment_manager: ExperimentManager instance

    Returns:
        Markdown string with comparison report

    """
    runs_df = experiment_manager.get_experiment_runs()

    if runs_df.empty:
        return "No runs found for comparison."

    # Group by model type and get best runs
    best_runs = runs_df.groupby("tags.model_type").first().reset_index()

    report = "# MLflow Experiment Comparison Report\n\n"
    report += f"## Experiment: {experiment_manager.experiment_name}\n\n"
    report += f"Total runs: {len(runs_df)}\n\n"

    report += "## Best Models by Type\n\n"
    report += "| Model Type | Accuracy | F1 Score | Run ID |\n"
    report += "|------------|----------|----------|--------|\n"

    for _, row in best_runs.iterrows():
        model_type = row.get("tags.model_type", "Unknown")
        accuracy = row.get("metrics.accuracy", "N/A")
        f1 = row.get("metrics.f1_score", "N/A")
        run_id = row.get("run_id", "N/A")

        report += f"| {model_type} | {accuracy} | {f1} | {run_id} |\n"

    report += "\n## Detailed Run Information\n\n"

    for _, row in runs_df.iterrows():
        run_id = row.get("run_id")
        model_type = row.get("tags.model_type", "Unknown")
        accuracy = row.get("metrics.accuracy", "N/A")

        report += f"### Run {run_id} ({model_type})\n"
        report += f"- Accuracy: {accuracy}\n"
        report += f"- Parameters: {dict(row.get('params', {}))}\n\n"

    return report
