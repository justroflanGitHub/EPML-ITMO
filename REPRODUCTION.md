# Reproduction Instructions - Complete Guide

## Overview

This document provides comprehensive instructions for reproducing all experiments, analyses, and results from the Iris Data Science Project. Follow these steps to achieve identical results to those documented in the project reports.

## Quick Start

For immediate reproduction, use the automated script:

```bash
# Clone and setup
git clone https://github.com/justroflanGitHub/EPML-ITMO.git
cd iris-data-science-project
git checkout hw_6

# Complete setup and reproduction
make reproduce-all
```

## Detailed Setup Instructions

### 1. Environment Setup

#### System Requirements
- **Operating System**: Linux, macOS, or Windows 10/11
- **Python**: 3.13 or higher
- **Memory**: Minimum 4GB RAM, 8GB recommended
- **Storage**: 2GB free space

#### Poetry Installation

```bash
# Method 1: Using pip
pip install poetry

# Method 2: Using official installer (recommended)
curl -sSL https://install.python-poetry.org | python3 -

# Verify installation
poetry --version
```

#### Repository Setup

```bash
# Clone repository
git clone https://github.com/justroflanGitHub/EPML-ITMO.git
cd iris-data-science-project

# Switch to the correct branch
git checkout hw_6

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Verify environment
python --version  # Should be 3.13+
poetry --version  # Should be 1.2+
```

### 2. Data Management with DVC

#### Initialize DVC (if not already done)

```bash
# Initialize DVC
dvc init

# Add remote storage (local example)
dvc remote add -d myremote data/remote

# Or add cloud storage (optional)
# dvc remote add -d s3remote s3://your-bucket/data
```

#### Data Operations

```bash
# Download and prepare data
dvc pull

# Or manually download using our script
python scripts/download_data.py

# Verify data integrity
python scripts/check_health.py
```

### 3. Configuration Management

#### Review Configuration

```bash
# Main configuration
cat config/config.yaml

# Hydra configurations
ls config/hydra/

# Model-specific configurations
cat config/hydra/model/random_forest.yaml
```

#### Modify Configuration (Optional)

To reproduce specific experiments, edit configuration files:

```bash
# Edit main config
vim config/config.yaml

# Edit model parameters
vim config/hydra/model/random_forest.yaml
```

## Reproducing Experiments

### Method 1: Automated Pipeline (Recommended)

```bash
# Run complete pipeline
make all

# Or use Snakemake directly
snakemake --cores all
```

### Method 2: Individual Steps

```bash
# Data preparation
snakemake data

# Training (all models)
snakemake train

# Evaluation
snakemake evaluate

# Report generation
snakemake reports
```

### Method 3: Individual Model Training

```bash
# Train specific models
python src/models/run_experiments.py

# Train single model
python src/models/train_model.py

# ClearML pipeline
python src/models/clearml_pipeline.py
```

### Method 4: Using Configuration Files

```bash
# Train with specific configuration
python src/run.py --config-name=iris config.model=random_forest

# Train with custom parameters
python src/run.py --config-path=config/hydra config.model=svm model.C=1.0
```

## Experiment Tracking with MLflow

### Start MLflow UI

```bash
# Start MLflow tracking server
mlflow ui --backend-store-uri sqlite:///models/mlruns/mlflow.db --host 0.0.0.0 --port 5000

# Or use the project's MLflow setup
cd src/models
python -m mlflow.ui --backend-store-uri ../../../models/mlruns/mlflow.db
```

### View Experiments

1. Open browser to `http://localhost:5000`
2. Select experiment: "iris_ml_experiments"
3. Compare runs and review metrics

### Reproduce Specific Experiments

To reproduce experiments with identical parameters:

```python
# Use the experiment runner
python src/models/run_experiments.py

# This will execute all 18 experiments with original parameters
```

## Report Generation

### Automated Report Generation

```bash
# Generate comprehensive reports
python scripts/generate_visual_reports.py

# Generate individual reports
python scripts/generate_report.py

# Generate comparison analysis
python src/models/compare_experiments.py
```

### Manual Report Generation

```bash
# Generate experiment summary
python -c "
from src.models.compare_experiments import compare_all_experiments
compare_all_experiments()
"

# Generate ClearML report
python src/models/train_model_clearml.py
```

## Validation and Verification

### Verify Results Match Expected Output

```bash
# Run validation script
python scripts/validate_config.py

# Check experiment consistency
python scripts/check_health.py

# Compare with baseline results
python -c "
import pandas as pd
results = pd.read_csv('reports/iris/random_forest/metrics.json')
print(f'Accuracy: {results[\"accuracy\"]:.4f}')
print('Expected: 0.9333')
"
```

### Expected Results

The reproduction should achieve these benchmark results:

| Model | Expected Accuracy | F1-Score |
|-------|------------------|----------|
| SVM_Linear | 100.00% | 1.0000 |
| LogisticRegression_L2 | 100.00% | 1.0000 |
| RandomForest_Minimal | 96.67% | 0.9666 |
| SVM_RBF | 96.67% | 0.9666 |

## Advanced Reproduction Scenarios

### Reproduce with Different Random Seeds

```bash
# Set specific random seed
export PYTHONHASHSEED=42
export RANDOM_STATE=42

# Run experiment
python src/models/run_experiments.py
```

### Reproduce with Modified Hyperparameters

```python
# Edit configuration file
vim config/hydra/model/random_forest.yaml

# Run with modified parameters
python src/run.py --config-name=iris config.model=random_forest
```

### Reproduce Cross-Validation Experiments

```bash
# Run cross-validation analysis
python scripts/cross_validation.py

# This generates detailed CV reports for all models
```

## Docker Reproduction

### Using Pre-built Image

```bash
# Pull and run with Docker
docker build -t iris-project .
docker run -it -p 5000:5000 -v $(pwd):/app iris-project bash

# Inside container
poetry install
python src/models/run_experiments.py
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# Run experiments in container
docker-compose exec iris-project python src/models/run_experiments.py

# View MLflow UI
open http://localhost:5000
```

## Troubleshooting Reproduction Issues

### Common Issues and Solutions

#### Poetry Installation Problems

```bash
# Clear cache and reinstall
poetry cache clear --all pypi .
poetry install --no-cache

# Check Python version compatibility
python --version  # Must be 3.13+
```

#### MLflow Database Issues

```bash
# Reset MLflow database
rm -f models/mlruns/mlflow.db
python src/models/run_experiments.py  # Will recreate database
```

#### DVC Data Issues

```bash
# Re-download data
dvc fetch
dvc checkout

# Or manually
rm -rf data/raw/iris.csv
python scripts/download_data.py
```

#### Permission Issues

```bash
# Fix file permissions
chmod +x scripts/*.py
chmod -R 755 .
```

### Verification Checklist

Use this checklist to ensure successful reproduction:

- [ ] Python 3.13+ installed
- [ ] Poetry installed and configured
- [ ] Repository cloned and checked out to `hw_6`
- [ ] All dependencies installed via `poetry install`
- [ ] Virtual environment activated
- [ ] Data downloaded and verified
- [ ] Configuration files accessible
- [ ] MLflow UI accessible at localhost:5000
- [ ] All 18 experiments completed successfully
- [ ] Reports generated successfully
- [ ] Results match expected benchmarks

## Performance Benchmarks

### Expected Execution Times

| Step | Expected Time | Hardware Assumptions |
|------|---------------|---------------------|
| Data Download | < 1 minute | Standard internet |
| Environment Setup | 2-5 minutes | SSD storage |
| All Experiments | 5-10 minutes | 4+ CPU cores |
| Report Generation | 1-2 minutes | Sufficient RAM |

### Memory Usage

- **Peak Usage**: ~2GB during cross-validation
- **Normal Usage**: ~500MB during training
- **MLflow Storage**: ~100MB for all experiments

## Advanced Features

### Reproducing Specific Analysis

```bash
# Feature importance analysis
python src/visualization/visualize.py --analysis=feature_importance

# Model comparison analysis
python src/models/compare_experiments.py --models=all

# Hyperparameter sensitivity analysis
python scripts/cross_validation.py --detailed=true
```

### Custom Experiment Reproduction

```python
# Create custom experiment configuration
import hydra
from hydra import compose, initialize
from omegaconf import DictConfig

with initialize(config_path="../config/hydra"):
    cfg = compose(config_name="config", overrides=["model=custom_model"])

# Run custom experiment
python src/run.py --config-path=config/hydra config.model=custom_model
```

## Getting Help

If reproduction fails:

1. Check the [troubleshooting section](#troubleshooting-reproduction-issues)
2. Review the [GitHub Issues](https://github.com/justroflanGitHub/EPML-ITMO/issues)
3. Contact: justroflanpochta@mail.ru

## Reproducibility Commitment

This project maintains full reproducibility through:

- **Versioned Dependencies**: All dependencies locked in `poetry.lock`
- **Versioned Data**: DVC for data versioning and tracking
- **Versioned Code**: Git tags for exact code snapshots
- **Deterministic Seeds**: Fixed random seeds throughout
- **Automated Pipelines**: Snakemake for reproducible workflows
- **Container Support**: Docker for environment isolation

---

**Last Updated**: December 25, 2025
**Version**: 2.0.0
**Maintained by**: Mikhail
