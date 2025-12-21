Iris Data Science Project
==============================

Comprehensive Data Science Workspace for Analyzing the Iris Dataset Using Modern Engineering Practices with Automated ML Pipelines, Data and Model Versioning

## Features

### HW4: Automated ML Pipelines (Latest)
- **Workflow Orchestration**: Snakemake for scalable, reproducible ML pipelines with DAG-based execution
- **Configuration Management**: Hydra for hierarchical configuration with validation and composition
- **Parallel Processing**: Multi-core execution with intelligent caching and dependency resolution
- **Model Comparison**: Automated training and evaluation of multiple algorithms (RF, SVM, LR, GB)
- **Monitoring & Notifications**: Health checks, performance monitoring, and Slack integration
- **Comprehensive Reporting**: Automated performance reports with cross-validation results

### HW2: Data & Model Versioning
- **Data Versioning**: DVC (Data Version Control) for tracking data changes and pipeline reproducibility
- **Model Versioning**: MLflow for experiment tracking, model registry, and deployment
- **Automated Pipeline**: Single-command pipeline execution with dependency management
- **Reproducible Environment**: Docker containerization and Poetry dependency management
- **Modern ML Practices**: Experiment tracking, model signatures, and automated testing

## Quick Start

### Prerequisites
- Python 3.13+
- pip (for dependency management)
- Git

### HW4: Automated Pipeline (Recommended)

1. Clone the repository and checkout HW4 branch:
```bash
git clone https://github.com/justroflanGitHub/EPML-ITMO.git
cd EPML-ITMO
git checkout hw_4
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the automated ML pipeline:
```bash
# Execute complete pipeline (downloads data, trains 4 models, evaluates, reports)
python -m snakemake --cores 4

# Dry run to see execution plan
python -m snakemake --dry-run --cores 1

# View pipeline performance report
cat reports/pipeline_report.md
```

### HW2: Traditional Pipeline

1. Checkout HW2 branch:
```bash
git checkout hw_2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the DVC pipeline:
```bash
dvc repro
```

## HW4 Pipeline Usage

### Pipeline Execution Options
```bash
# Run specific pipeline stages
python -m snakemake train_model --cores 4          # Train models only
python -m snakemake evaluate_model --cores 4       # Evaluate models only
python -m snakemake generate_pipeline_report       # Generate reports

# Clean intermediate files
python -m snakemake clean

# View pipeline DAG visualization
python -m snakemake dag
```

### Configuration Management
The pipeline uses Hydra for flexible configuration:

```bash
# View available configurations
python scripts/validate_config.py

# Run with different algorithms
# Edit config/hydra/config.yaml to modify algorithms list
```

### Monitoring & Results
```bash
# View performance summary
cat reports/performance_summary.json

# Check pipeline health
cat reports/health_check.json

# View detailed metrics for each algorithm
ls reports/iris/*/metrics.json
```

## HW2 Legacy Usage

### Data Pipeline
- **Download data**: `python src/data/make_dataset.py data/raw/iris.csv`
- **Run full pipeline**: `dvc repro`
- **Push data to remote**: `dvc push`

### Model Training & Tracking
- **Train model**: `python src/models/train_model.py data/raw/iris.csv models/model.joblib`
- **View experiments**: `mlflow ui --backend-store-uri models/mlruns`
- **Open browser**: http://localhost:5000

## Results Summary

HW4 Pipeline Performance (Latest Run):

| Algorithm | Test Accuracy | CV Accuracy (Mean ± Std) |
|-----------|---------------|---------------------------|
| SVM | 0.967 | 0.975 ± 0.020 |
| Logistic Regression | 0.967 | 0.967 ± 0.017 |
| Gradient Boosting | 0.967 | 0.967 ± 0.017 |
| Random Forest | 0.900 | 0.950 ± 0.017 |

**Best Model**: SVM with 96.7% accuracy

## Documentation

### HW4 Documentation
- [HW4 Implementation Report](HW4_REPORT.md) - Complete automated pipeline documentation
- [Pipeline Architecture Details](HW4_REPORT.md#pipeline-architecture) - Technical implementation details
- [Configuration Guide](HW4_REPORT.md#configuration-management-with-hydra) - Hydra configuration system

### HW2 Documentation
- [Detailed Setup Report](VERSIONING_REPORT.md) - Complete implementation details
- [Reproduction Instructions](REPRODUCTION.md) - Step-by-step guide for setup and usage

## Tools Overview

### Snakemake (HW4)
- **Purpose**: Workflow orchestration and pipeline management
- **Features**: DAG-based execution, parallel processing, caching
- **Usage**: `python -m snakemake --cores N`

### Hydra (HW4)
- **Purpose**: Hierarchical configuration management
- **Features**: Configuration validation, composition, inheritance
- **Files**: `config/hydra/` directory structure

### DVC (HW2)
- **Purpose**: Data version control and pipeline tracking
- **Features**: Data versioning, large file support, remote storage
- **Usage**: `dvc add`, `dvc repro`, `dvc push`

### MLflow (HW2/HW4)
- **Purpose**: Experiment tracking and model management
- **Features**: Parameter logging, metric tracking, model registry
- **Usage**: `mlflow ui` for web interface

## Project Organization

```
├── LICENSE
├── README.md              <- This file
├── HW4_REPORT.md          <- HW4 implementation documentation
├── VERSIONING_REPORT.md   <- HW2 implementation documentation
├── REPRODUCTION.md        <- Setup and usage instructions
├── data/                  <- Data directory structure
│   ├── raw/              <- Original data
│   ├── processed/        <- Cleaned and processed data
│   └── remote/           <- DVC remote storage
├── models/               <- Trained models and artifacts
│   └── mlruns/           <- MLflow experiment data
├── reports/              <- Generated reports and metrics
├── config/               <- HW4 Hydra configuration
│   ├── hydra/           <- Hierarchical config structure
│   └── composed/         <- Generated composed configs
├── rules/                <- HW4 Snakemake rule definitions
├── scripts/              <- HW4 Python execution scripts
├── src/                  <- Source code
│   ├── data/            <- Data processing scripts
│   ├── models/          <- Model training scripts
│   └── visualization/   <- Visualization scripts
├── Snakefile             <- HW4 main workflow definition
├── dvc.yaml             <- HW2 pipeline definition
├── pyproject.toml       <- Poetry configuration
├── requirements.txt     <- Python dependencies
├── Dockerfile           <- Container definition
└── tox.ini             <- Testing configuration
```

## Development & Contributing

### Running Tests
```bash
# HW4 pipeline tests
python -m snakemake --cores 1  # Will validate all dependencies

# HW2 pipeline tests
dvc repro  # Will validate DVC pipeline
```

### Code Quality
The project uses pre-commit hooks for code quality:
- Black for code formatting
- isort for import sorting
- Ruff for linting
- MyPy for type checking

### Adding New Algorithms (HW4)
1. Create algorithm configuration in `config/hydra/model/`
2. Add algorithm to `config/config.yaml` algorithms list
3. The pipeline will automatically include it in training

## Docker Support

```bash
# Build container
docker build -t iris-project .

# Run HW4 pipeline in container
docker run -it iris-project python -m snakemake --cores 4

# Run HW2 pipeline in container
docker run -it iris-project dvc repro
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Branch Information

- **hw_4**: Latest HW4 implementation with Snakemake + Hydra automated pipelines
- **hw_2**: HW2 implementation with DVC + MLflow data/model versioning
- **main**: Project root with basic structure

For the most advanced features, use the `hw_4` branch.

---

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
