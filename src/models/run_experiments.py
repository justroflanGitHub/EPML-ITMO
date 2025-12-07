"""Run multiple ML experiments with different algorithms for Iris dataset.

This script runs 15+ experiments with various ML algorithms and hyperparameters,
logging everything to MLflow for comprehensive experiment tracking.
"""

import logging
from pathlib import Path

import mlflow
import pandas as pd
from mlflow_utils import (
    ExperimentManager,
    log_classification_metrics,
    log_model_info,
    setup_mlflow_tracking,
)
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

logger = logging.getLogger(__name__)


def load_and_preprocess_data(
    data_path: str,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Load and preprocess the Iris dataset.

    Args:
        data_path: Path to the processed data file

    Returns:
        Tuple of (X_train, X_test, y_train, y_test)

    """
    df = pd.read_csv(data_path)
    X = df.drop(["target", "target_name"], axis=1)
    y = df["target"]

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index
    )
    X_test_scaled = pd.DataFrame(
        scaler.transform(X_test), columns=X_test.columns, index=X_test.index
    )

    return X_train_scaled, X_test_scaled, y_train, y_test


def get_model_configs() -> list[dict]:
    """Get configurations for different ML models and hyperparameters.

    Returns:
        List of model configurations

    """
    return [
        # 1-3: Random Forest variations
        {
            "name": "RandomForest_Default",
            "model": RandomForestClassifier(random_state=42),
            "params": {},
        },
        {
            "name": "RandomForest_Tuned",
            "model": RandomForestClassifier(random_state=42),
            "params": {"n_estimators": [50, 100, 200], "max_depth": [None, 10, 20]},
        },
        {
            "name": "RandomForest_Minimal",
            "model": RandomForestClassifier(
                n_estimators=10, max_depth=3, random_state=42
            ),
            "params": {},
        },
        # 4-6: SVM variations
        {
            "name": "SVM_Linear",
            "model": SVC(kernel="linear", random_state=42),
            "params": {"C": [0.1, 1.0, 10.0]},
        },
        {
            "name": "SVM_RBF",
            "model": SVC(kernel="rbf", random_state=42),
            "params": {"C": [0.1, 1.0, 10.0], "gamma": ["scale", "auto"]},
        },
        {
            "name": "SVM_Poly",
            "model": SVC(kernel="poly", degree=3, random_state=42),
            "params": {"C": [0.1, 1.0, 10.0]},
        },
        # 7-9: Tree-based models
        {
            "name": "DecisionTree_Default",
            "model": DecisionTreeClassifier(random_state=42),
            "params": {},
        },
        {
            "name": "DecisionTree_Tuned",
            "model": DecisionTreeClassifier(random_state=42),
            "params": {"max_depth": [None, 5, 10], "min_samples_split": [2, 5, 10]},
        },
        {
            "name": "GradientBoosting",
            "model": GradientBoostingClassifier(random_state=42),
            "params": {"n_estimators": [50, 100], "learning_rate": [0.1, 0.2]},
        },
        # 10-12: Linear models
        {
            "name": "LogisticRegression_Default",
            "model": LogisticRegression(random_state=42, max_iter=1000),
            "params": {},
        },
        {
            "name": "LogisticRegression_L1",
            "model": LogisticRegression(
                penalty="l1", solver="liblinear", random_state=42, max_iter=1000
            ),
            "params": {"C": [0.1, 1.0, 10.0]},
        },
        {
            "name": "LogisticRegression_L2",
            "model": LogisticRegression(penalty="l2", random_state=42, max_iter=1000),
            "params": {"C": [0.1, 1.0, 10.0]},
        },
        # 13-15: Other algorithms
        {
            "name": "KNeighbors_Default",
            "model": KNeighborsClassifier(),
            "params": {"n_neighbors": [3, 5, 7]},
        },
        {"name": "NaiveBayes", "model": GaussianNB(), "params": {}},
        {
            "name": "MLPClassifier",
            "model": MLPClassifier(random_state=42, max_iter=1000),
            "params": {
                "hidden_layer_sizes": [(50,), (100,), (50, 50)],
                "alpha": [0.0001, 0.001],
            },
        },
        # 16-18: Ensemble methods
        {
            "name": "AdaBoost",
            "model": AdaBoostClassifier(random_state=42),
            "params": {"n_estimators": [50, 100], "learning_rate": [0.1, 1.0]},
        },
        {
            "name": "RandomForest_ExtraTrees",
            "model": RandomForestClassifier(criterion="entropy", random_state=42),
            "params": {"n_estimators": [50, 100], "max_depth": [None, 10]},
        },
        {
            "name": "GradientBoosting_Tuned",
            "model": GradientBoostingClassifier(random_state=42),
            "params": {
                "n_estimators": [100, 200],
                "max_depth": [3, 5],
                "learning_rate": [0.05, 0.1],
            },
        },
    ]


def run_single_experiment(
    model_config: dict,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    experiment_name: str = "iris_experiment",
) -> dict:
    """Run a single ML experiment with MLflow tracking.

    Args:
        model_config: Configuration for the model
        X_train: Training features
        X_test: Test features
        y_train: Training labels
        y_test: Test labels
        experiment_name: Name of the MLflow experiment

    Returns:
        Dictionary with experiment results

    """
    model_name = model_config["name"]
    model = model_config["model"]
    params = model_config["params"]

    with mlflow.start_run(run_name=model_name):
        # Set tags
        mlflow.set_tag("model_type", type(model).__name__)
        mlflow.set_tag("experiment_type", "single_model")
        mlflow.set_tag("dataset", "iris")

        try:
            # Perform grid search if parameters are provided
            if params:
                grid_search = GridSearchCV(
                    model, params, cv=3, scoring="accuracy", n_jobs=-1
                )
                grid_search.fit(X_train, y_train)
                best_model = grid_search.best_estimator_

                # Log best parameters
                for param_name, param_value in grid_search.best_params_.items():
                    mlflow.log_param(f"best_{param_name}", param_value)

                # Log CV results
                mlflow.log_metric("cv_mean_score", grid_search.best_score_)
                mlflow.log_metric(
                    "cv_std_score",
                    grid_search.cv_results_["std_test_score"][grid_search.best_index_],
                )

            else:
                best_model = model
                best_model.fit(X_train, y_train)

            # Log model info
            log_model_info(best_model)

            # Make predictions
            y_pred = best_model.predict(X_test)

            # Log metrics
            metrics = log_classification_metrics(y_test, y_pred)

            # Log model artifact
            mlflow.sklearn.log_model(best_model, "model")

            # Log feature importance if available
            if hasattr(best_model, "feature_importances_"):
                for i, importance in enumerate(best_model.feature_importances_):
                    mlflow.log_metric(f"feature_importance_{i}", importance)

            logger.info(
                f"Completed experiment: {model_name} with accuracy: {metrics['accuracy']:.4f}"
            )

            return {
                "model_name": model_name,
                "model": best_model,
                "metrics": metrics,
                "status": "success",
            }

        except Exception as e:
            mlflow.set_tag("status", "failed")
            mlflow.set_tag("error", str(e))
            logger.error(f"Experiment {model_name} failed: {e}")

            return {"model_name": model_name, "error": str(e), "status": "failed"}


def run_all_experiments(
    data_path: str, experiment_name: str = "iris_experiment"
) -> list[dict]:
    """Run all configured experiments.

    Args:
        data_path: Path to the processed data
        experiment_name: Name of the MLflow experiment

    Returns:
        List of experiment results

    """
    # Set up MLflow
    setup_mlflow_tracking(experiment_name=experiment_name)

    # Load and preprocess data
    logger.info("Loading and preprocessing data...")
    X_train, X_test, y_train, y_test = load_and_preprocess_data(data_path)

    # Get model configurations
    model_configs = get_model_configs()
    logger.info(f"Running {len(model_configs)} experiments...")

    results = []

    # Run each experiment
    for i, config in enumerate(model_configs, 1):
        logger.info(f"Running experiment {i}/{len(model_configs)}: {config['name']}")

        result = run_single_experiment(
            config, X_train, X_test, y_train, y_test, experiment_name
        )
        results.append(result)

        # Log progress
        successful_runs = len([r for r in results if r.get("status") == "success"])
        logger.info(
            f"Progress: {successful_runs}/{len(model_configs)} experiments completed successfully"
        )

    logger.info(f"All experiments completed. {len(results)} total runs.")
    return results


def create_summary_report(
    results: list[dict], experiment_manager: ExperimentManager
) -> str:
    """Create a comprehensive summary report of all experiments.

    Args:
        results: List of experiment results
        experiment_manager: ExperimentManager instance

    Returns:
        Markdown string with summary report

    """
    successful_results = [r for r in results if r.get("status") == "success"]

    report = "# Iris Dataset ML Experiments Summary Report\n\n"

    report += "## Overview\n\n"
    report += f"- Total experiments: {len(results)}\n"
    report += f"- Successful experiments: {len(successful_results)}\n"
    report += f"- Failed experiments: {len(results) - len(successful_results)}\n\n"

    if successful_results:
        report += "## Model Performance Comparison\n\n"
        report += "| Model | Accuracy | F1 Score | Precision | Recall |\n"
        report += "|-------|----------|----------|-----------|--------|\n"

        # Sort by accuracy
        sorted_results = sorted(
            successful_results,
            key=lambda x: x.get("metrics", {}).get("accuracy", 0),
            reverse=True,
        )

        for result in sorted_results:
            metrics = result.get("metrics", {})
            model_name = result.get("model_name", "Unknown")
            accuracy = metrics.get("accuracy", "N/A")
            f1 = metrics.get("f1_score", "N/A")
            precision = metrics.get("precision", "N/A")
            recall = metrics.get("recall", "N/A")

            report += f"| {model_name} | {accuracy} | {f1} | {precision} | {recall} |\n"

        # Best model
        best_result = sorted_results[0]
        report += "\n## Best Performing Model\n\n"
        report += f"**{best_result['model_name']}** with accuracy: {best_result['metrics']['accuracy']:.4f}\n\n"

    # MLflow comparison
    try:
        from mlflow_utils import create_experiment_comparison_report

        comparison_report = create_experiment_comparison_report(experiment_manager)
        report += "\n## MLflow Experiment Comparison\n\n"
        report += comparison_report
    except Exception as e:
        report += f"\n## MLflow Comparison Error\n\nFailed to generate MLflow comparison: {e}\n\n"

    return report


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Data path
    project_dir = Path(__file__).resolve().parents[2]
    data_path = project_dir / "data" / "processed" / "iris.csv"

    if not data_path.exists():
        logger.error(f"Data file not found: {data_path}")
        # Try to create data first
        from src.data.make_dataset import main as make_dataset

        make_dataset(str(data_path))

    # Run experiments
    experiment_name = "iris_ml_experiments"
    results = run_all_experiments(str(data_path), experiment_name)

    # Create summary report
    experiment_manager = ExperimentManager(experiment_name)
    summary_report = create_summary_report(results, experiment_manager)

    # Save report
    report_path = project_dir / "reports" / "experiment_summary.md"
    report_path.parent.mkdir(exist_ok=True)

    with open(report_path, "w") as f:
        f.write(summary_report)

    logger.info(f"Summary report saved to: {report_path}")

    # Print summary
    successful_runs = len([r for r in results if r.get("status") == "success"])
    logger.info(f"Experiments completed: {successful_runs}/{len(results)} successful")
