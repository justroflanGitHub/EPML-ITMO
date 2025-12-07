# Reproduction Instructions

## Setup Environment

1. Install Poetry if not installed:
   ```bash
   pip install poetry
   ```

2. Clone the repository and navigate to the project directory.

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Data Versioning with DVC

1. Initialize DVC (already done):
   ```bash
   dvc init
   ```

2. Add remote storage (local):
   ```bash
   dvc remote add -d myremote data/remote
   ```

3. Pull data (if remote exists):
   ```bash
   dvc pull
   ```

## Run the Pipeline

To reproduce the entire pipeline:

```bash
dvc repro
```

This will:
- Download the iris dataset
- Train the model
- Log to MLflow

## Model Versioning with MLflow

1. Start MLflow UI to view experiments:
   ```bash
   mlflow ui --backend-store-uri models/mlruns
   ```

2. Open http://localhost:5000 to view runs and models.

## Docker

Build and run the container:

```bash
docker build -t iris-project .
docker run -p 8888:8888 iris-project
```

Note: The Dockerfile has a placeholder CMD. Update it as needed.

## Dependency Versions

All dependencies are pinned in `pyproject.toml` and locked in `poetry.lock`.
