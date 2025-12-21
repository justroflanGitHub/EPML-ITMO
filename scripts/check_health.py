#!/usr/bin/env python3
"""Check pipeline health and data integrity."""

import json
import os
from datetime import datetime


def main():
    health_status = {
        "timestamp": datetime.now().isoformat(),
        "overall_status": "healthy",
        "checks": {},
        "issues": [],
    }

    datasets = ["iris"]
    algorithms = ["random_forest", "svm", "logistic_regression", "gradient_boosting"]

    # Check data integrity
    for dataset in datasets:
        data_path = f"data/processed/{dataset}"
        if os.path.exists(f"{data_path}/train.csv") and os.path.exists(
            f"{data_path}/test.csv"
        ):
            health_status["checks"][f"data_{dataset}"] = "present"
        else:
            health_status["checks"][f"data_{dataset}"] = "missing"
            health_status["issues"].append(f"Missing processed data for {dataset}")
            health_status["overall_status"] = "unhealthy"

    # Check model outputs
    for dataset in datasets:
        for algorithm in algorithms:
            model_path = f"models/{dataset}/{algorithm}/model.pkl"
            metrics_path = f"reports/{dataset}/{algorithm}/metrics.json"

            if os.path.exists(model_path):
                health_status["checks"][f"model_{dataset}_{algorithm}"] = "present"
            else:
                health_status["checks"][f"model_{dataset}_{algorithm}"] = "missing"
                health_status["issues"].append(
                    f"Missing model for {dataset}/{algorithm}"
                )
                health_status["overall_status"] = "unhealthy"

            if os.path.exists(metrics_path):
                health_status["checks"][f"metrics_{dataset}_{algorithm}"] = "present"

                # Check metrics values
                try:
                    with open(metrics_path) as f:
                        metrics = json.load(f)
                    if not (0 <= metrics.get("accuracy", -1) <= 1):
                        health_status["issues"].append(
                            f"Invalid accuracy for {dataset}/{algorithm}"
                        )
                        health_status["overall_status"] = "unhealthy"
                except:
                    health_status["issues"].append(
                        f"Corrupted metrics for {dataset}/{algorithm}"
                    )
                    health_status["overall_status"] = "unhealthy"
            else:
                health_status["checks"][f"metrics_{dataset}_{algorithm}"] = "missing"
                health_status["issues"].append(
                    f"Missing metrics for {dataset}/{algorithm}"
                )
                health_status["overall_status"] = "unhealthy"

    # Save health check results
    with open("reports/health_check.json", "w") as f:
        json.dump(health_status, f, indent=2)

    status_emoji = "✅" if health_status["overall_status"] == "healthy" else "❌"
    print(f"{status_emoji} Pipeline health check completed")
    print(f"Status: {health_status['overall_status']}")
    if health_status["issues"]:
        print("Issues found:")
        for issue in health_status["issues"]:
            print(f"  - {issue}")


if __name__ == "__main__":
    main()
