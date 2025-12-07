Iris Data Science Project
==============================

Comprehensive Data Science Workspace for Analyzing the Iris Dataset Using Modern Engineering Practices with Data and Model Versioning

## Features

- **Data Versioning**: DVC (Data Version Control) for tracking data changes and pipeline reproducibility
- **Model Versioning**: MLflow for experiment tracking, model registry, and deployment
- **Automated Pipeline**: Single-command pipeline execution with dependency management
- **Reproducible Environment**: Docker containerization and Poetry dependency management
- **Modern ML Practices**: Experiment tracking, model signatures, and automated testing

## Quick Start

### Prerequisites
- Python 3.13+
- Poetry (for dependency management)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/justroflanGitHub/EPML-ITMO.git
cd EPML-ITMO
git checkout hw_2
```

2. Install dependencies:
```bash
poetry install
```

3. Run the complete pipeline:
```bash
poetry run dvc repro
```

## Usage

### Data Pipeline
- **Download data**: `poetry run python src/data/make_dataset.py data/raw/iris.csv`
- **Run full pipeline**: `poetry run dvc repro`
- **Push data to remote**: `poetry run dvc push`

### Model Training & Tracking
- **Train model**: `poetry run python src/models/train_model.py data/raw/iris.csv models/model.joblib`
- **View experiments**: `poetry run mlflow ui --backend-store-uri models/mlruns`
- **Open browser**: http://localhost:5000

### Docker
```bash
# Build container
docker build -t iris-project .

# Run pipeline in container
docker run iris-project
```

## Documentation

- [Detailed Setup Report](VERSIONING_REPORT.md) - Complete implementation details
- [Reproduction Instructions](REPRODUCTION.md) - Step-by-step guide for setup and usage

## Versioning Tools

### DVC (Data Version Control)
- Tracks data files and pipeline dependencies
- Supports large file storage with remote backends
- Integrates with Git for code versioning

### MLflow
- Experiment tracking with parameters, metrics, and artifacts
- Model registry for production deployment
- UI for comparing experiments and models

## Project Organization

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── VERSIONING_REPORT.md <- Detailed setup report for data and model versioning
    ├── REPRODUCTION.md    <- Step-by-step reproduction instructions
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   ├── raw            <- The original, immutable data dump.
    │   └── remote         <- DVC remote storage directory
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │   └── mlruns         <- MLflow experiment tracking data
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── pyproject.toml     <- Poetry configuration with dependencies
    ├── poetry.lock        <- Poetry lock file for reproducible dependencies
    ├── dvc.yaml           <- DVC pipeline definition
    ├── dvc.lock           <- DVC pipeline lock file
    ├── Dockerfile         <- Docker container definition
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   ├── run.py         <- Main entry point for running pipeline or Jupyter
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
