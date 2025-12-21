"""
Snakemake workflow for ML pipeline orchestration.

This workflow implements automated ML pipelines with:
- Data preprocessing
- Model training with different algorithms
- Evaluation and metrics collection
- Parallel execution and caching
"""

import os
from pathlib import Path

# Configuration
configfile: "config/config.yaml"

# Include Hydra configurations
include: "rules/hydra.smk"
include: "rules/data.smk"
include: "rules/train.smk"
include: "rules/evaluate.smk"
include: "rules/monitor.smk"

# Default target
rule all:
    input:
        "config/validation_report.json",
        expand("config/composed/{dataset}_{algorithm}.yaml",
               dataset=config["datasets"],
               algorithm=config["algorithms"]),
        expand("data/raw/{dataset}.csv", dataset=config["datasets"]),
        expand("data/processed/{dataset}/train.csv", dataset=config["datasets"]),
        expand("data/processed/{dataset}/test.csv", dataset=config["datasets"]),
        expand("models/{dataset}/{algorithm}/model.pkl",
               dataset=config["datasets"],
               algorithm=config["algorithms"]),
        expand("reports/{dataset}/{algorithm}/metrics.json",
               dataset=config["datasets"],
               algorithm=config["algorithms"]),
        expand("reports/{dataset}/{algorithm}/cv_results.json",
               dataset=config["datasets"],
               algorithm=config["algorithms"]),
        "reports/pipeline_report.md",
        "reports/performance_summary.json",
        "reports/notification_log.json",
        "reports/health_check.json"

# Clean rule
rule clean:
    shell:
        """
        rm -rf data/processed/*
        rm -rf models/*
        rm -rf reports/*
        """

# Clean cache
rule clean_cache:
    shell:
        "snakemake --cleanup-metadata"

# DAG visualization
rule dag:
    output:
        "reports/dag.png"
    shell:
        "snakemake --dag | dot -Tpng > reports/dag.png"

# Rule graph
rule rulegraph:
    output:
        "reports/rulegraph.png"
    shell:
        "snakemake --rulegraph | dot -Tpng > reports/rulegraph.png"
