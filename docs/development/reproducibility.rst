Reproducibility Guide
====================

This guide ensures that all experiments and results in the Iris Data Science Project can be reproduced consistently across different environments and over time.

Core Principles
---------------

The project follows these reproducibility principles:

1. **Version Control**: All code, data, and configurations are version controlled
2. **Environment Specification**: Exact dependency versions are pinned
3. **Random Seed Management**: Random operations use fixed seeds
4. **Containerization**: Docker provides consistent runtime environments
5. **Documentation**: All steps are thoroughly documented

Environment Setup
-----------------

Python Environment
~~~~~~~~~~~~~~~~~~

Use Poetry for consistent Python environment management:

.. code-block:: bash

   # Install Poetry
   curl -sSL https://install.python-poetry.org | python3 -

   # Install project dependencies
   poetry install

   # Activate environment
   poetry shell

   # Verify environment
   python --version
   pip list

System Dependencies
~~~~~~~~~~~~~~~~~~~

Install system-level dependencies:

.. code-block:: bash

   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install -y python3-dev build-essential

   # macOS
   brew install python@3.13

   # Windows (using Chocolatey)
   choco install python --version=3.13.0

Docker Environment
~~~~~~~~~~~~~~~~~~

Use Docker for complete environment reproducibility:

.. code-block:: bash

   # Build reproducible environment
   docker build --no-cache -t iris-ml:reproducible .

   # Run in container
   docker run -it --rm iris-ml:reproducible bash

   # Verify environment
   docker run --rm iris-ml:reproducible python -c "import sys; print(sys.version)"

Data Management
---------------

Dataset Versioning
~~~~~~~~~~~~~~~~~~

Use DVC for data versioning:

.. code-block:: bash

   # Initialize DVC
   dvc init

   # Track data
   dvc add data/raw/iris.csv

   # Commit data version
   dvc commit

   # Push data to remote storage
   dvc remote add -d myremote s3://my-bucket/data
   dvc push

Data Download
~~~~~~~~~~~~~

Reproducible data acquisition:

.. code-block:: bash

   # Download exact dataset version
   python scripts/download_data.py --version 1.0

   # Verify data integrity
   sha256sum data/raw/iris.csv

Data Preprocessing
~~~~~~~~~~~~~~~~~~

Documented preprocessing pipeline:

.. code-block:: python

   from src.data.make_dataset import load_iris_data, preprocess_data
   import hashlib

   # Load data
   data = load_iris_data()

   # Verify data integrity
   data_hash = hashlib.sha256(str(data).encode()).hexdigest()
   expected_hash = "a1b2c3d4e5f6..."  # From documentation
   assert data_hash == expected_hash, "Data integrity check failed"

   # Preprocess with fixed parameters
   X_train, X_test, y_train, y_test = preprocess_data(
       data,
       test_size=0.2,
       random_state=42
   )

Code Versioning
---------------

Git Version Control
~~~~~~~~~~~~~~~~~~~

Use Git for complete code versioning:

.. code-block:: bash

   # Check exact commit
   git log --oneline -1

   # Verify clean working directory
   git status

   # Show all changes
   git diff

   # List all files with their versions
   git ls-files | xargs ls -la

Dependency Pinning
~~~~~~~~~~~~~~~~~~

Exact dependency versions in pyproject.toml:

.. code-block:: toml

   [tool.poetry.dependencies]
   python = "^3.13"
   pandas = "2.2.3"      # Exact version
   numpy = "2.2.1"       # Exact version
   scikit-learn = "1.6.0" # Exact version
   mlflow = "^2.17.0"    # Compatible range

Lock File
~~~~~~~~~

Use Poetry lock file for exact reproducibility:

.. code-block:: bash

   # Install exact versions from lock file
   poetry install

   # Verify lock file integrity
   sha256sum poetry.lock

   # Export exact requirements
   poetry export -f requirements.txt --output requirements.txt

Experiment Reproducibility
---------------------------

Random Seed Management
~~~~~~~~~~~~~~~~~~~~~~~

Fixed random seeds throughout the pipeline:

.. code-block:: python

   import numpy as np
   import random

   # Set global random seed
   RANDOM_SEED = 42

   # Set all random number generators
   np.random.seed(RANDOM_SEED)
   random.seed(RANDOM_SEED)

   # Scikit-learn random state
   from sklearn.ensemble import RandomForestClassifier
   model = RandomForestClassifier(random_state=RANDOM_SEED)

   # PyTorch random seed (if used)
   import torch
   torch.manual_seed(RANDOM_SEED)
   torch.cuda.manual_seed(RANDOM_SEED)

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

Use Hydra for reproducible configurations:

.. code-block:: python

   from omegaconf import OmegaConf

   # Load exact configuration
   cfg = OmegaConf.load("config/config.yaml")

   # Verify configuration integrity
   cfg_hash = hashlib.sha256(str(cfg).encode()).hexdigest()
   assert cfg_hash == "expected_config_hash"

   # Run experiment with exact config
   run_experiment(cfg)

Experiment Tracking
~~~~~~~~~~~~~~~~~~~

MLflow for experiment reproducibility:

.. code-block:: python

   import mlflow

   # Set exact experiment
   mlflow.set_experiment("iris_reproducible_experiment")

   with mlflow.start_run():
       # Log exact parameters
       mlflow.log_param("random_seed", 42)
       mlflow.log_param("model_type", "random_forest")
       mlflow.log_param("n_estimators", 100)

       # Run experiment
       model, metrics = train_model(X_train, y_train)

       # Log exact results
       mlflow.log_metrics(metrics)
       mlflow.sklearn.log_model(model, "model")

ClearML for advanced reproducibility:

.. code-block:: python

   from clearml import Task

   # Create reproducible task
   task = Task.init(
       project_name="Iris Reproducible Experiments",
       task_name="rf_experiment_v1"
   )

   # Log exact code version
   task.set_code_repo(
       url="https://github.com/justroflanGitHub/EPML-ITMO.git",
       commit="abc123def456"
   )

   # Connect exact configuration
   task.connect({"random_seed": 42, "model_config": model_config})

Pipeline Reproducibility
-------------------------

Snakemake Workflows
~~~~~~~~~~~~~~~~~~~

Use Snakemake for reproducible pipelines:

.. code-block:: bash

   # Run with exact configuration
   snakemake --config random_seed=42 model=random_forest

   # Verify pipeline integrity
   snakemake --dry-run

   # Generate pipeline report
   snakemake --report report.html

Makefile Automation
~~~~~~~~~~~~~~~~~~~

Documented automation scripts:

.. code-block:: makefile

   .PHONY: reproducible_experiment
   reproducible_experiment:
       @echo "Running reproducible experiment..."
       poetry run python src/run.py \
           random_seed=42 \
           experiment.name=reproducible_run \
           model=random_forest

Docker Pipeline
~~~~~~~~~~~~~~~

Containerized pipeline execution:

.. code-block:: bash

   # Run complete reproducible pipeline
   docker run --rm \
       -v $(pwd):/app \
       -e RANDOM_SEED=42 \
       iris-ml:reproducible \
       make all

   # Verify container integrity
   docker inspect iris-ml:reproducible

Results Reproduction
---------------------

Model Loading
~~~~~~~~~~~~~

Load exact model versions:

.. code-block:: python

   import joblib
   import hashlib

   # Load model
   model = joblib.load('models/iris_model.pkl')

   # Verify model integrity
   model_hash = hashlib.sha256(joblib.dumps(model)).hexdigest()
   expected_hash = "model_hash_from_documentation"
   assert model_hash == expected_hash

Prediction Reproduction
~~~~~~~~~~~~~~~~~~~~~~~

Reproduce exact predictions:

.. code-block:: python

   import numpy as np

   # Exact test input
   test_input = np.array([[5.1, 3.5, 1.4, 0.2]])

   # Make prediction with exact model
   prediction = model.predict(test_input)
   probabilities = model.predict_proba(test_input)

   # Verify results match documentation
   assert prediction[0] == 0  # setosa
   assert abs(probabilities[0][0] - 0.98) < 0.01  # 98% confidence

Report Reproduction
~~~~~~~~~~~~~~~~~~~

Regenerate exact reports:

.. code-block:: bash

   # Generate report with exact parameters
   python scripts/generate_report.py \
       --experiment reproducible_run \
       --format markdown \
       --seed 42

   # Verify report integrity
   sha256sum reports/reproducible_report.md

Validation and Testing
-----------------------

Unit Tests
~~~~~~~~~~

Comprehensive test suite:

.. code-block:: bash

   # Run all tests
   python -m pytest tests/ -v

   # Run with coverage
   python -m pytest tests/ --cov=src --cov-report=html

Integration Tests
~~~~~~~~~~~~~~~~~

End-to-end pipeline tests:

.. code-block:: python

   def test_full_pipeline_reproducibility():
       """Test that full pipeline produces identical results."""

       # Run pipeline twice with same seed
       result1 = run_full_pipeline(seed=42)
       result2 = run_full_pipeline(seed=42)

       # Verify identical results
       assert result1['accuracy'] == result2['accuracy']
       assert result1['model_hash'] == result2['model_hash']
       assert result1['report_hash'] == result2['report_hash']

Data Validation
~~~~~~~~~~~~~~~

Validate data integrity:

.. code-block:: python

   def validate_dataset_integrity(data_path):
       """Validate dataset hasn't changed."""

       # Calculate data hash
       with open(data_path, 'rb') as f:
           data_hash = hashlib.sha256(f.read()).hexdigest()

       # Check against known good hash
       known_hashes = {
           "iris.csv": "a1b2c3d4e5f6...",
           "processed_data.pkl": "g7h8i9j0k1l2..."
       }

       assert data_hash == known_hashes[data_path.split('/')[-1]]

Model Validation
~~~~~~~~~~~~~~~~

Validate model performance:

.. code-block:: python

   def validate_model_performance(model, X_test, y_test):
       """Validate model meets performance requirements."""

       from sklearn.metrics import accuracy_score

       predictions = model.predict(X_test)
       accuracy = accuracy_score(y_test, predictions)

       # Check against documented performance
       documented_accuracy = 0.967  # From reproducibility documentation
       assert abs(accuracy - documented_accuracy) < 0.01

       return True

CI/CD Reproducibility
---------------------

GitHub Actions
~~~~~~~~~~~~~~

Automated reproducibility testing:

.. code-block:: yaml

   name: Reproducibility Test
   on: [push, pull_request]

   jobs:
     test-reproducibility:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v2
       - name: Set up Python
         uses: actions/setup-python@v2
         with:
           python-version: '3.13'
       - name: Install dependencies
         run: poetry install
       - name: Run reproducibility test
         run: python tests/test_reproducibility.py
       - name: Validate results
         run: python scripts/validate_reproducibility.py

Docker Testing
~~~~~~~~~~~~~~

Container-based testing:

.. code-block:: bash

   # Test in multiple environments
   docker run --rm python:3.9-slim bash -c "
       pip install poetry &&
       poetry install &&
       python tests/test_reproducibility.py
   "

   docker run --rm python:3.11-slim bash -c "
       pip install poetry &&
       poetry install &&
       python tests/test_reproducibility.py
   "

Documentation
-------------

Reproducibility Statement
~~~~~~~~~~~~~~~~~~~~~~~~~

Include in all reports:

.. code-block:: markdown

   ## Reproducibility Statement

   This experiment can be reproduced using:

   - **Code Version**: Commit `abc123def456`
   - **Data Version**: DVC hash `def789ghi012`
   - **Environment**: Python 3.13.0, Poetry environment
   - **Random Seed**: 42
   - **Configuration**: See `config/config.yaml`

   To reproduce:
   ```bash
   git checkout abc123def456
   dvc checkout
   poetry install
   python src/run.py random_seed=42
   ```

Reproducibility Checklist
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

   - [ ] All random seeds are fixed
   - [ ] Dependencies are pinned to exact versions
   - [ ] Code is committed to Git
   - [ ] Data is versioned with DVC
   - [ ] Environment is containerized
   - [ ] Configuration is documented
   - [ ] Results include reproducibility instructions
   - [ ] Validation tests pass

Archival and Long-term Preservation
------------------------------------

Data Archival
~~~~~~~~~~~~~

Long-term data preservation:

.. code-block:: bash

   # Create archival package
   tar -czf iris_reproducible_archive_20251225.tar.gz \
       --exclude='.git' \
       --exclude='__pycache__' \
       .

   # Include reproducibility manifest
   cat > MANIFEST.md << EOF
   # Iris Dataset Reproducibility Archive

   Created: December 25, 2025
   Version: 1.0.0

   ## Contents
   - Complete source code
   - Dataset and preprocessing scripts
   - Trained models and artifacts
   - Experiment configurations
   - Documentation and reports

   ## Reproduction Instructions
   See docs/development/reproducibility.rst

   ## Checksums
   $(sha256sum iris_reproducible_archive_20251225.tar.gz)
   EOF

Code Archival
~~~~~~~~~~~~~

Preserve code for long-term access:

.. code-block:: bash

   # Create code archive with metadata
   git archive --format=tar.gz --prefix=iris-code/ \
       --output=iris_code_archive_20251225.tar.gz \
       HEAD

   # Include software bill of materials
   poetry export > sbom_requirements.txt

Model Archival
~~~~~~~~~~~~~~

Preserve trained models:

.. code-block:: bash

   # Archive models with metadata
   mkdir -p model_archive
   cp models/*.pkl model_archive/

   # Create model manifest
   cat > model_archive/MANIFEST.json << EOF
   {
     "archive_date": "2025-12-25",
     "models": [
       {
         "name": "iris_random_forest.pkl",
         "algorithm": "Random Forest",
         "accuracy": 0.967,
         "training_date": "2025-12-25",
         "parameters": {"n_estimators": 100, "random_state": 42}
       }
     ],
     "reproducibility": {
       "code_commit": "$(git rev-parse HEAD)",
       "data_version": "$(dvc list data)",
       "environment": "Python 3.13.0, Poetry"
     }
   }
   EOF

Verification Scripts
---------------------

Automated Verification
~~~~~~~~~~~~~~~~~~~~~~

Scripts to verify reproducibility:

.. code-block:: python

   # reproducibility_verifier.py
   import subprocess
   import hashlib
   import json

   def verify_reproducibility():
       """Comprehensive reproducibility verification."""

       results = {}

       # Check Git status
       git_status = subprocess.run(['git', 'status', '--porcelain'],
                                   capture_output=True, text=True)
       results['clean_repo'] = len(git_status.stdout.strip()) == 0

       # Verify dependencies
       poetry_check = subprocess.run(['poetry', 'check'],
                                     capture_output=True, text=True)
       results['dependencies_valid'] = poetry_check.returncode == 0

       # Check data integrity
       with open('data/raw/iris.csv', 'rb') as f:
           data_hash = hashlib.sha256(f.read()).hexdigest()
       results['data_integrity'] = data_hash == EXPECTED_DATA_HASH

       # Run experiment and verify results
       subprocess.run(['python', 'src/run.py', 'random_seed=42'])
       with open('models/iris_model.pkl', 'rb') as f:
           model_hash = hashlib.sha256(f.read()).hexdigest()
       results['model_reproducibility'] = model_hash == EXPECTED_MODEL_HASH

       return results

   if __name__ == "__main__":
       results = verify_reproducibility()
       print(json.dumps(results, indent=2))

       if all(results.values()):
           print("✓ All reproducibility checks passed!")
       else:
           print("✗ Some reproducibility checks failed!")
           for check, passed in results.items():
               if not passed:
                   print(f"  - {check}: FAILED")

Continuous Monitoring
~~~~~~~~~~~~~~~~~~~~~

Monitor reproducibility over time:

.. code-block:: bash

   # Daily reproducibility check
   cat > /etc/cron.daily/reproducibility_check << 'EOF'
   #!/bin/bash
   cd /path/to/iris-project
   python scripts/verify_reproducibility.py > reproducibility_check_$(date +%Y%m%d).log
   EOF

   chmod +x /etc/cron.daily/reproducibility_check

This comprehensive reproducibility guide ensures that all aspects of the Iris Data Science Project can be consistently reproduced across different environments and time periods.
