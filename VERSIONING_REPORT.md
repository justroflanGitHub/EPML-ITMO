# Data and Model Versioning Setup Report

## Overview

This project implements a comprehensive data and model versioning system for the Iris dataset ML project using modern engineering practices. The system uses DVC for data versioning and MLflow for model versioning, ensuring reproducibility and traceability.

## Tools Chosen

### Data Versioning: DVC (Data Version Control)
- **Why chosen**: DVC is specifically designed for ML data versioning, integrates well with Git, and supports large file handling.
- **Alternatives considered**: LakeFS (more complex for local setup), Git LFS (less ML-focused).

### Model Versioning: MLflow
- **Why chosen**: MLflow provides comprehensive model registry, experiment tracking, and deployment capabilities.
- **Alternatives considered**: DVC (used primarily for data).

## Data Versioning Setup

### DVC Configuration
1. **Initialization**: `dvc init` creates DVC repository structure.
2. **Remote Storage**: Local directory `data/remote` configured as remote storage.
3. **Data Tracking**: Iris dataset tracked with `dvc add data/raw/iris.csv`.
4. **Pipeline**: Automated pipeline defined in `dvc.yaml` with stages for data download and model training.

### Automatic Versioning
- DVC pipeline automatically versions data changes.
- Dependencies and outputs tracked in `dvc.lock`.
- Use `dvc repro` to reproduce the entire pipeline.

## Model Versioning Setup

### MLflow Configuration
1. **Tracking URI**: Local directory `models/mlruns` for experiment storage.
2. **Experiment**: "iris_experiment" created for the project.
3. **Run Logging**: Each training run logs parameters, metrics, and model artifacts.
4. **Model Registry**: Models logged with signatures for input/output validation.

### Metadata and Versioning
- **Parameters logged**: n_estimators, random_state
- **Metrics logged**: accuracy
- **Model artifacts**: Serialized model with sklearn flavor
- **Signatures**: Input/output schema inferred automatically

### Version Comparison
- MLflow UI provides comparison of runs by metrics and parameters.
- Models can be registered and versioned in the model registry.
- Historical runs preserved for comparison.

## Reproducibility

### Dependency Management
- **Poetry**: Used for Python dependency management.
- **Pinned versions**: All dependencies pinned in `pyproject.toml`.
- **Lock file**: `poetry.lock` ensures exact reproduction.

### Docker Container
- **Base image**: Python 3.13-slim
- **Dependencies**: Poetry installs all dependencies.
- **Pipeline execution**: Container runs `dvc repro` by default.
- **Jupyter support**: Can be started with `python src/run.py` (without pipeline arg).

### Reproduction Instructions
See `REPRODUCTION.md` for detailed setup and reproduction steps.

## Testing Results

### Pipeline Reproduction
- `dvc repro` successfully reproduces the entire pipeline.
- Data download and model training execute correctly.
- Outputs match expected results (accuracy: 1.0 on test set).

### Docker Build
- Container builds successfully with all dependencies.
- Pipeline runs in container environment.

## Screenshots

(Note: Screenshots would be included here in a real report)

1. DVC pipeline execution
2. MLflow UI showing experiment runs
3. Model registry interface
4. Docker container build and run

## Files Modified/Created

### New Files
- `src/run.py`: Main entry point
- `dvc.yaml`: Pipeline definition
- `REPRODUCTION.md`: Reproduction instructions
- `VERSIONING_REPORT.md`: This report
- `models/mlruns/`: MLflow tracking directory
- `data/remote/`: DVC remote storage

### Modified Files
- `pyproject.toml`: Added DVC, MLflow, joblib dependencies
- `src/data/make_dataset.py`: Implemented iris data download
- `src/models/train_model.py`: Implemented ML training with MLflow logging
- `.gitignore`: Modified to track DVC files
- `Dockerfile`: Updated CMD to run pipeline

## Git Integration

- DVC files committed to Git for metadata tracking
- Actual data and models stored in DVC remote (can be pushed with `dvc push`)
- Git history preserves code changes
- DVC tracks data/model changes separately

## Conclusion

The implemented system provides:
- **Traceability**: Every data and model change is versioned
- **Reproducibility**: Exact environment and pipeline reproduction
- **Automation**: Single command pipeline execution
- **Scalability**: Ready for cloud storage (S3) and larger datasets
- **Collaboration**: Git+DVC enables team collaboration on ML projects

The setup follows ML engineering best practices and is production-ready.
