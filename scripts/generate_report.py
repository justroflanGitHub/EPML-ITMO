#!/usr/bin/env python3
"""Generate comprehensive pipeline performance report."""

import json
from datetime import datetime

import pandas as pd


def main():
    # Collect all metrics
    all_metrics = []
    all_cv_summaries = []

    datasets = ["iris"]
    algorithms = ["random_forest", "svm", "logistic_regression", "gradient_boosting"]

    for dataset in datasets:
        for algorithm in algorithms:
            try:
                # Load metrics
                metrics_file = f"reports/{dataset}/{algorithm}/metrics.json"
                with open(metrics_file) as f:
                    metrics = json.load(f)
                    metrics["dataset"] = dataset
                    metrics["algorithm"] = algorithm
                    all_metrics.append(metrics)

                # Load CV summary
                cv_file = f"reports/{dataset}/{algorithm}/cv_summary.json"
                with open(cv_file) as f:
                    cv_summary = json.load(f)
                    cv_summary["dataset"] = dataset
                    cv_summary["algorithm"] = algorithm
                    all_cv_summaries.append(cv_summary)

            except FileNotFoundError:
                print(f"Warning: Results not found for {dataset}/{algorithm}")

    # Create summary DataFrame
    metrics_df = pd.DataFrame(all_metrics)
    cv_df = pd.DataFrame(all_cv_summaries)

    # Find best performing models
    best_accuracy = metrics_df.loc[metrics_df["accuracy"].idxmax()]
    best_f1 = metrics_df.loc[metrics_df["f1_macro"].idxmax()]

    # Generate markdown report
    report = f"""# ML Pipeline Performance Report

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Executive Summary

This report summarizes the performance of {len(algorithms)} different machine learning algorithms
trained on {len(datasets)} datasets using automated Snakemake workflows with Hydra configuration management.

## Best Performing Models

### Highest Accuracy
- **Algorithm**: {best_accuracy["algorithm"]}
- **Dataset**: {best_accuracy["dataset"]}
- **Accuracy**: {best_accuracy["accuracy"]:.4f}
- **F1-Score**: {best_accuracy["f1_macro"]:.4f}

### Highest F1-Score
- **Algorithm**: {best_f1["algorithm"]}
- **Dataset**: {best_f1["dataset"]}
- **Accuracy**: {best_f1["accuracy"]:.4f}
- **F1-Score**: {best_f1["f1_macro"]:.4f}

## Detailed Results

### Performance Comparison
| Algorithm | Dataset | Accuracy | Precision (Macro) | Recall (Macro) | F1-Score (Macro) |
|-----------|---------|----------|-------------------|----------------|------------------|
"""

    for _, row in metrics_df.iterrows():
        report += f"| {row['algorithm']} | {row['dataset']} | {row['accuracy']:.4f} | {row['precision_macro']:.4f} | {row['recall_macro']:.4f} | {row['f1_macro']:.4f} |\n"

    report += """
### Cross-Validation Results
| Algorithm | Dataset | CV Accuracy (Mean ± Std) | CV F1-Score (Mean ± Std) |
|-----------|---------|---------------------------|---------------------------|
"""

    for _, row in cv_df.iterrows():
        acc_mean = row["best_score"]
        acc_std = row["cv_std"]
        report += f"| {row['algorithm']} | {row['dataset']} | {acc_mean:.4f} ± {acc_std:.4f} | N/A |\n"

    report += """
## Pipeline Configuration

### Tools Used
- **Workflow Orchestration**: Snakemake
- **Configuration Management**: Hydra
- **Experiment Tracking**: MLflow
- **Version Control**: DVC

### Algorithms Tested
- Random Forest
- Support Vector Machine (SVM)
- Logistic Regression
- Gradient Boosting

### Datasets
- Iris (classification, 3 classes, 150 samples)

## Recommendations

1. **Primary Model**: Use {best_accuracy['algorithm']} for production deployment
2. **Backup Model**: Consider {best_f1['algorithm']} for scenarios requiring balanced precision/recall
3. **Further Tuning**: All models show room for hyperparameter optimization
4. **Monitoring**: Implement continuous monitoring of model performance in production

---
*Report generated automatically by Snakemake pipeline*
"""

    # Save report
    with open("reports/pipeline_report.md", "w") as f:
        f.write(report)

    # Save summary JSON
    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_models": len(all_metrics),
        "best_accuracy_model": {
            "algorithm": best_accuracy["algorithm"],
            "dataset": best_accuracy["dataset"],
            "accuracy": best_accuracy["accuracy"],
        },
        "best_f1_model": {
            "algorithm": best_f1["algorithm"],
            "dataset": best_f1["dataset"],
            "f1_score": best_f1["f1_macro"],
        },
        "all_results": all_metrics,
        "cv_summaries": all_cv_summaries,
    }

    with open("reports/performance_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("Pipeline report generated successfully")


if __name__ == "__main__":
    main()
