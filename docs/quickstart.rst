Quick Start
===========

This guide will get you up and running with the Iris Data Science Project in minutes.

Running the Complete Pipeline
------------------------------

The easiest way to get started is to run the complete MLOps pipeline:

.. code-block:: bash

   # Make sure you're in the project directory
   cd iris-data-science-project

   # Run everything (data processing, training, evaluation, reporting)
   make all

This single command will:

1. Download and process the Iris dataset
2. Train multiple machine learning models
3. Evaluate model performance
4. Generate comprehensive reports
5. Track experiments with MLflow and ClearML

Step-by-Step Quick Start
-------------------------

If you prefer to run things step by step:

1. Prepare the Data
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Download and preprocess data
   make data

2. Train Models
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Train all models
   make train

   # Or train specific models
   make train MODEL=random_forest
   make train MODEL=svm
   make train MODEL=logistic_regression
   make train MODEL=gradient_boosting

3. Evaluate Performance
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Evaluate all trained models
   make evaluate

4. Generate Reports
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Generate comprehensive reports
   make report

Interactive Exploration
-----------------------

Launch Jupyter Notebook for interactive exploration:

.. code-block:: bash

   # Start Jupyter server
   jupyter notebook

   # Or with Poetry
   poetry run jupyter notebook

Then open ``notebooks/exploration.ipynb`` to explore the data and models.

Using Docker
------------

For a completely reproducible environment:

.. code-block:: bash

   # Build the Docker image
   docker build -t iris-ml .

   # Run the complete pipeline
   docker run --rm -v $(pwd):/app iris-ml make all

   # Or run interactively
   docker run -it --rm -v $(pwd):/app iris-ml bash

Experiment Tracking
-------------------

View your experiments in the tracking UIs:

**MLflow UI:**

.. code-block:: bash

   # Start MLflow server
   mlflow ui

   # Open http://localhost:5000 in your browser

**ClearML Web UI:**

Visit your ClearML server (usually https://app.clear.ml) or your self-hosted instance.

Running Individual Components
-----------------------------

You can also run individual pipeline components:

.. code-block:: bash

   # Data operations
   python scripts/download_data.py
   python scripts/preprocess_data.py

   # Model training
   python scripts/train_model.py --config config/hydra/model/random_forest.yaml

   # Evaluation
   python scripts/evaluate_model.py

   # Cross-validation
   python scripts/cross_validation.py

   # Report generation
   python scripts/generate_report.py

Configuration Examples
----------------------

Train a model with custom parameters:

.. code-block:: bash

   # Using Hydra configuration
   python src/run.py +experiment=random_forest max_depth=10 n_estimators=200

   # Using Snakemake
   snakemake --config model=random_forest

Monitor Pipeline Health
-----------------------

Check the health of your MLOps pipeline:

.. code-block:: bash

   # Run health checks
   python scripts/check_health.py

   # Monitor pipeline status
   python scripts/monitor_pipeline.py

Next Steps
----------

Now that you've run your first pipeline:

* Explore the generated reports in the ``reports/`` directory
* Check experiment results in MLflow/ClearML UIs
* Modify configurations in ``config/`` directory
* Read the full :doc:`usage` guide for advanced features
* Learn about :doc:`configuration` options
* Set up automated :doc:`experiments`

Troubleshooting
---------------

**Pipeline Fails:**

Check the logs and ensure all dependencies are installed:

.. code-block:: bash

   # Check installation
   poetry check

   # Reinstall dependencies
   poetry install --no-cache

**MLflow/ClearML Issues:**

Ensure tracking servers are running:

.. code-block:: bash

   # Check MLflow
   curl http://localhost:5000/health

   # Check ClearML configuration
   clearml-task --help

**Memory Issues:**

If you encounter memory problems, try running smaller models:

.. code-block:: bash

   # Run with limited models
   make train MODELS="random_forest logistic_regression"
