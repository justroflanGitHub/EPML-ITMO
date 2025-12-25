#!/usr/bin/env python3
"""Compare ClearML Experiments

This script provides functionality to compare multiple ClearML experiments,
analyze their performance, and generate comparison reports.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from clearml import Task


def get_project_tasks(project_name: str, task_type: str = None) -> list[Task]:
    """Get all tasks from a ClearML project."""
    try:
        # Get tasks from project
        tasks = Task.get_tasks(
            project_name=project_name, task_name=None, allow_archived=False
        )

        if task_type:
            tasks = [t for t in tasks if t.data.type == task_type]

        return tasks
    except Exception as e:
        logging.error(f"Failed to get tasks from project {project_name}: {e}")
        return []


def extract_task_metrics(task: Task) -> dict[str, Any]:
    """Extract metrics and parameters from a ClearML task."""
    try:
        metrics = {}
        params = {}

        # Get scalar metrics
        scalar_metrics = task.get_reported_scalars()
        for metric_name, metric_data in scalar_metrics.items():
            if metric_data and metric_data.get("y"):
                # Get the latest value
                values = metric_data["y"]
                metrics[metric_name] = values[-1] if values else None

        # Get parameters
        task_params = task.get_parameters()
        for param_name, param_value in task_params.items():
            if param_value is not None:
                params[param_name] = param_value

        # Get task metadata
        metadata = {
            "task_id": task.id,
            "task_name": task.name,
            "project": task.project,
            "status": task.status,
            "created": task.data.created,
            "completed": getattr(task.data, "completed", None),
            "duration": None,
        }

        # Calculate duration if completed
        if metadata["completed"] and metadata["created"]:
            try:
                created_time = datetime.fromisoformat(
                    metadata["created"].replace("Z", "+00:00")
                )
                completed_time = datetime.fromisoformat(
                    metadata["completed"].replace("Z", "+00:00")
                )
                metadata["duration"] = (completed_time - created_time).total_seconds()
            except:
                pass

        return {"metadata": metadata, "metrics": metrics, "parameters": params}

    except Exception as e:
        logging.error(f"Failed to extract data from task {task.id}: {e}")
        return {}


def compare_experiments(
    project_name: str, metric_names: list[str] = None
) -> pd.DataFrame:
    """Compare experiments from a ClearML project."""
    if metric_names is None:
        metric_names = ["accuracy"]

    logging.info(f"Comparing experiments in project: {project_name}")

    # Get all training tasks
    tasks = get_project_tasks(project_name, task_type="training")

    if not tasks:
        logging.warning(f"No training tasks found in project {project_name}")
        return pd.DataFrame()

    logging.info(f"Found {len(tasks)} training tasks")

    # Extract data from each task
    experiments_data = []
    for task in tasks:
        task_data = extract_task_metrics(task)

        if task_data:
            # Flatten data for DataFrame
            row = {}
            row.update(task_data["metadata"])
            row.update(task_data["metrics"])
            row.update({f"param_{k}": v for k, v in task_data["parameters"].items()})

            experiments_data.append(row)

    if not experiments_data:
        logging.warning("No experiment data could be extracted")
        return pd.DataFrame()

    # Create DataFrame
    df = pd.DataFrame(experiments_data)

    # Sort by primary metric (descending)
    primary_metric = metric_names[0] if metric_names else "accuracy"
    if primary_metric in df.columns:
        df = df.sort_values(primary_metric, ascending=False)

    return df


def generate_comparison_report(
    comparison_df: pd.DataFrame, project_name: str, output_path: str = None
) -> str:
    """Generate a comparison report from experiment data."""
    if comparison_df.empty:
        return "No experiments to compare"

    report_lines = []
    report_lines.append("# ClearML Experiments Comparison Report")
    report_lines.append(f"**Project:** {project_name}")
    report_lines.append(
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    report_lines.append("")

    # Summary statistics
    report_lines.append("## Summary Statistics")
    report_lines.append(f"- Total experiments: {len(comparison_df)}")
    report_lines.append(
        f"- Completed experiments: {comparison_df['status'].eq('completed').sum()}"
    )

    if "accuracy" in comparison_df.columns:
        best_accuracy = comparison_df["accuracy"].max()
        avg_accuracy = comparison_df["accuracy"].mean()
        report_lines.append(f"- Best accuracy: {best_accuracy:.4f}")
        report_lines.append(f"- Average accuracy: {avg_accuracy:.4f}")

    report_lines.append("")

    # Top experiments table
    report_lines.append("## Top 10 Experiments")

    # Select relevant columns
    display_cols = ["task_name", "accuracy", "status", "duration"]
    display_cols = [col for col in display_cols if col in comparison_df.columns]

    if display_cols:
        top_experiments = comparison_df.head(10)[display_cols].copy()

        # Format duration
        if "duration" in top_experiments.columns:
            top_experiments["duration"] = top_experiments["duration"].apply(
                lambda x: f"{x:.1f}s" if pd.notnull(x) else "N/A"
            )

        # Format accuracy
        if "accuracy" in top_experiments.columns:
            top_experiments["accuracy"] = top_experiments["accuracy"].apply(
                lambda x: f"{x:.4f}" if pd.notnull(x) else "N/A"
            )

        report_lines.append(top_experiments.to_markdown(index=False))
    else:
        report_lines.append("No relevant metrics found for comparison")

    report_lines.append("")

    # Model type distribution
    if "param_model_type" in comparison_df.columns:
        report_lines.append("## Model Type Distribution")
        model_counts = comparison_df["param_model_type"].value_counts()
        for model_type, count in model_counts.items():
            report_lines.append(f"- {model_type}: {count} experiments")
        report_lines.append("")

    # Performance analysis
    if "accuracy" in comparison_df.columns:
        report_lines.append("## Performance Analysis")

        # Best performing models
        best_models = comparison_df.nlargest(3, "accuracy")[["task_name", "accuracy"]]
        report_lines.append("### Best Performing Models")
        for _, row in best_models.iterrows():
            report_lines.append(f"- **{row['task_name']}**: {row['accuracy']:.4f}")
        report_lines.append("")

        # Accuracy distribution
        report_lines.append("### Accuracy Distribution")
        accuracy_stats = comparison_df["accuracy"].describe()
        report_lines.append(f"- Mean: {accuracy_stats['mean']:.4f}")
        report_lines.append(f"- Std: {accuracy_stats['std']:.4f}")
        report_lines.append(f"- Min: {accuracy_stats['min']:.4f}")
        report_lines.append(f"- Max: {accuracy_stats['max']:.4f}")
        report_lines.append("")

    # Recommendations
    report_lines.append("## Recommendations")

    if "accuracy" in comparison_df.columns and len(comparison_df) > 1:
        best_task = comparison_df.loc[comparison_df["accuracy"].idxmax()]
        report_lines.append(
            f"1. **Best Model**: {best_task['task_name']} (Accuracy: {best_task['accuracy']:.4f})"
        )

        # Check if there are significant performance differences
        accuracy_std = comparison_df["accuracy"].std()
        if accuracy_std > 0.01:  # More than 1% variation
            report_lines.append(
                "2. **Model Selection**: Consider hyperparameter tuning for the best performing model type"
            )
        else:
            report_lines.append(
                "2. **Model Selection**: Performance is consistent across models"
            )

    report_lines.append(
        "3. **Next Steps**: Review model artifacts and consider deployment of the best performing model"
    )

    # Save report if output path provided
    report_content = "\n".join(report_lines)

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            f.write(report_content)
        logging.info(f"Comparison report saved to: {output_path}")

    return report_content


def log_comparison_to_clearml(
    comparison_df: pd.DataFrame, project_name: str, report_content: str
):
    """Log the comparison results to ClearML."""
    try:
        # Create a comparison task
        task = Task.init(
            project_name=project_name,
            task_name=f"experiments_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            task_type=Task.TaskTypes.data_processing,
            reuse_last_task_id=False,
        )

        # Upload comparison data
        task.upload_artifact("comparison_dataframe", comparison_df.to_dict("records"))
        task.upload_artifact("comparison_report", report_content)

        # Log summary metrics
        if "accuracy" in comparison_df.columns:
            from clearml import Logger

            logger = Logger.current_logger()

            logger.report_scalar(
                "best_accuracy", "summary", comparison_df["accuracy"].max(), iteration=0
            )
            logger.report_scalar(
                "avg_accuracy", "summary", comparison_df["accuracy"].mean(), iteration=0
            )
            logger.report_scalar(
                "experiments_count", "summary", len(comparison_df), iteration=0
            )

        logging.info(f"Comparison logged to ClearML task: {task.id}")
        task.close()

    except Exception as e:
        logging.error(f"Failed to log comparison to ClearML: {e}")


def main():
    """Main function for experiment comparison."""
    import argparse

    parser = argparse.ArgumentParser(description="Compare ClearML experiments")
    parser.add_argument(
        "--project", default="Iris Data Science Project", help="ClearML project name"
    )
    parser.add_argument(
        "--metrics", nargs="+", default=["accuracy"], help="Metrics to compare"
    )
    parser.add_argument("--output", help="Output path for comparison report")
    parser.add_argument(
        "--log-to-clearml",
        action="store_true",
        help="Log comparison results to ClearML",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Compare experiments
    comparison_df = compare_experiments(args.project, args.metrics)

    if comparison_df.empty:
        logging.error("No experiments found for comparison")
        return

    # Generate report
    report = generate_comparison_report(comparison_df, args.project, args.output)

    print("\n" + "=" * 80)
    print("EXPERIMENTS COMPARISON REPORT")
    print("=" * 80)
    print(report)
    print("=" * 80)

    # Log to ClearML if requested
    if args.log_to_clearml:
        log_comparison_to_clearml(comparison_df, args.project, report)


if __name__ == "__main__":
    main()
