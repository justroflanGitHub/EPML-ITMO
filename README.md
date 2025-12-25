Iris Data Science Project
==============================

Comprehensive Data Science Workspace for Analyzing the Iris Dataset Using Modern Engineering Practices with Automated ML Pipelines, Data and Model Versioning

## Features

### HW6: Complete Documentation and Reporting System (Latest)
- **Technical Documentation**: Sphinx-based documentation with MyST parser for comprehensive project docs
- **GitHub Pages Deployment**: Automated CI/CD pipeline for documentation publishing
- **Experiment Reports**: Comprehensive analysis of 18+ ML algorithms with visualizations and comparisons
- **Automated Report Generation**: Visual report generation system with charts and performance metrics
- **Reproducibility**: Complete setup instructions, Docker support, and environment validation
- **MLOps Integration**: Combined ClearML, MLflow, DVC, Hydra, and Snakemake workflows

### HW5: ClearML MLOps Integration
- **Experiment Tracking**: ClearML for comprehensive experiment logging, parameter tracking, and artifact management
- **Model Management**: Automatic model versioning, registration, and deployment with metadata tracking
- **Pipeline Orchestration**: ClearML pipelines for end-to-end ML workflow automation with dependency management
- **Real-time Monitoring**: Pipeline status monitoring, automated alerts, and performance tracking
- **Experiment Comparison**: Cross-experiment analysis with performance visualization and recommendations
- **Multi-framework Support**: Native support for scikit-learn models with extensible architecture
- **Production Ready**: Enterprise-grade MLOps solution with audit trails and compliance features

### HW4: Automated ML Pipelines
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
- ClearML account (optional, for hosted service)

### HW6: Complete Documentation and Reporting System (Most Advanced)

1. Clone the repository and checkout HW6 branch:
```bash
git clone https://github.com/justroflanGitHub/EPML-ITMO.git
cd iris-data-science-project
git checkout hw_6
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Build documentation:
```bash
cd docs
python -m sphinx -b html . _build/html
# Documentation available at docs/_build/html/index.html
```

4. Generate automated reports:
```bash
python scripts/generate_visual_reports.py
# View reports in reports/ directory
```

### HW5: ClearML MLOps Integration

1. Clone the repository and checkout HW5 branch:
```bash
git clone https://github.com/justroflanGitHub/EPML-ITMO.git
cd EPML-ITMO
git checkout hw_5
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Setup ClearML (optional, for full functionality):
```bash
# Set environment variables
export CLEARML_API_ACCESS_KEY='your_access_key'
export CLEARML_API_SECRET_KEY='your_secret_key'

# Initialize ClearML
python scripts/setup_clearml.py
```

4. Run ClearML experiment:
```bash
# Train model with ClearML tracking
python src/models/train_model_clearml.py data/processed/iris_processed.csv models/clearml_model.pkl --model-type random_forest

# Run ClearML pipeline
python src/models/clearml_pipeline.py --dataset data/processed/iris_processed.csv --models random_forest svm

# Compare experiments
python src/models/compare_experiments.py --project "Iris Data Science Project"
```

### HW4: Automated Pipeline

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

## HW6 Documentation and Reporting

### Documentation System
```bash
# Build Sphinx documentation
cd docs
python -m sphinx -b html . _build/html

# View documentation
open docs/_build/html/index.html
```

### Automated Report Generation
```bash
# Generate comprehensive reports with visualizations
python scripts/generate_visual_reports.py

# View generated reports
ls reports/
# - experiments_comprehensive_report.md
# - auto_report_summary.json
# - automated_report.md
# - figures/feature_importance.png
```

### Experiment Analysis
```bash
# Run comprehensive experiment comparison
python src/models/run_experiments.py

# View MLflow experiments
mlflow ui --backend-store-uri models/mlruns
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
python -m snakemake dag > pipeline_dag.png
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

HW6 Documentation System includes comprehensive analysis of 18+ ML algorithms with detailed performance comparisons, visualizations, and automated report generation.

## Documentation

### HW6 Documentation
- [HW6 Documentation System](docs/_build/html/index.html) - Complete Sphinx documentation
- [Comprehensive Experiment Reports](reports/experiments_comprehensive_report.md) - Analysis of 18+ ML algorithms
- [Automated Report Generation](scripts/generate_visual_reports.py) - Visual report system
- [Reproduction Guide](REPRODUCTION.md) - Complete setup and usage instructions

### HW5 Documentation
- [ClearML MLOps Implementation Report](reports/ClearML_MLOps_Report.md) - Complete ClearML integration documentation
- [Experiment Tracking Guide](reports/ClearML_MLOps_Report.md#experiment-tracking) - ClearML experiment management
- [Pipeline Orchestration](reports/ClearML_MLOps_Report.md#pipeline-orchestration) - Automated ML workflows
- [Monitoring & Alerts](reports/ClearML_MLOps_Report.md#monitoring-and-notifications) - Real-time pipeline monitoring

### HW4 Documentation
- [HW4 Implementation Report](HW4_REPORT.md) - Complete automated pipeline documentation
- [Pipeline Architecture Details](HW4_REPORT.md#pipeline-architecture) - Technical implementation details
- [Configuration Guide](HW4_REPORT.md#configuration-management-with-hydra) - Hydra configuration system

### HW2 Documentation
- [Detailed Setup Report](VERSIONING_REPORT.md) - Complete implementation details
- [Reproduction Instructions](REPRODUCTION.md) - Step-by-step guide for setup and usage

## Tools Overview

### HW6 Documentation Tools
- **Sphinx**: Documentation generation with MyST parser for Markdown support
- **GitHub Actions**: Automated documentation deployment to GitHub Pages
- **Automated Reporting**: Custom scripts for visual report generation with matplotlib/seaborn

### ClearML (HW5)
- **Purpose**: Enterprise MLOps platform for experiment tracking and pipeline orchestration
- **Features**: Real-time monitoring, model management, automated pipelines, production deployment
- **Usage**: Web interface at https://app.clear.ml, programmatic API for automation

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
├── reports/
│   ├── experiments_comprehensive_report.md  <- HW6 comprehensive analysis
│   ├── auto_report_summary.json             <- HW6 automated summary
│   ├── automated_report.md                  <- HW6 generated report
│   ├── figures/                             <- HW6 visualization charts
│   ├── ClearML_MLOps_Report.md              <- HW5 implementation documentation
│   ├── HW4_REPORT.md                        <- HW4 implementation documentation
│   └── VERSIONING_REPORT.md                 <- HW2 implementation documentation
├── REPRODUCTION.md        <- Setup and usage instructions
├── docs/                  <- HW6 Sphinx documentation
│   ├── _build/html/      <- Generated documentation
│   ├── conf.py           <- Sphinx configuration
│   └── [other rst/md files]
├── data/                  <- Data directory structure
│   ├── raw/              <- Original data
│   ├── processed/        <- Cleaned and processed data
│   └── remote/           <- DVC remote storage
├── models/               <- Trained models and artifacts
│   ├── mlruns/           <- MLflow experiment data
│   └── clearml_artifacts/ <- ClearML artifacts storage
├── config/               <- Configuration files
│   ├── clearml/          <- HW5 ClearML configuration
│   │   └── config.yaml
│   ├── hydra/           <- HW4 Hydra configuration
│   └── composed/         <- Generated composed configs
├── rules/                <- HW4 Snakemake rule definitions
├── scripts/              <- Python execution scripts
│   ├── generate_visual_reports.py           <- HW6 report generation
│   ├── setup_clearml.py                     <- HW5 ClearML initialization
│   └── [other scripts]                      <- HW4 pipeline scripts
├── src/                  <- Source code
│   ├── data/            <- Data processing scripts
│   ├── models/          <- Model training scripts
│   │   ├── train_model_clearml.py           <- HW5 ClearML training
│   │   ├── compare_experiments.py           <- HW5 experiment comparison
│   │   ├── clearml_pipeline.py              <- HW5 pipeline orchestration
│   │   ├── pipeline_monitor.py              <- HW5 monitoring system
│   │   ├── run_experiments.py               <- HW6 comprehensive experiments
│   └── visualization/   <- Visualization scripts
├── Snakefile             <- HW4 main workflow definition
├── dvc.yaml             <- HW2 pipeline definition
├── .clearml.conf        <- HW5 ClearML client configuration
├── pyproject.toml       <- Poetry configuration
├── requirements.txt     <- Python dependencies
├── Dockerfile           <- Container definition
└── tox.ini             <- Testing configuration
```

## Development & Contributing

### Running Tests
```bash
# HW6 documentation tests
cd docs && python -m sphinx -b html . _build/html

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

# Run HW6 documentation
docker run -it iris-project bash -c "cd docs && python -m sphinx -b html . _build/html"

# Run HW4 pipeline in container
docker run -it iris-project python -m snakemake --cores 4

# Run HW2 pipeline in container
docker run -it iris-project dvc repro
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Branch Information

- **hw_6**: Latest HW6 implementation with complete documentation and reporting system (Most Advanced)
- **hw_5**: HW5 implementation with ClearML MLOps integration
- **hw_4**: HW4 implementation with Snakemake + Hydra automated pipelines
- **hw_2**: HW2 implementation with DVC + MLflow data/model versioning
- **main**: Project root with basic structure

For the most complete MLOps and documentation features, use the `hw_6` branch.

---

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
