Configuration Guide
==================

The Iris Data Science Project uses Hydra for flexible configuration management. This guide explains how to configure experiments, models, and pipeline settings.

Configuration Structure
------------------------

The project uses a hierarchical configuration system:

.. code-block::

   config/
   ├── config.yaml                    # Main configuration
   ├── hydra/
   │   ├── config.yaml               # Hydra base config
   │   ├── data/
   │   │   └── iris.yaml            # Dataset configuration
   │   ├── model/                    # Model configurations
   │   │   ├── random_forest.yaml
   │   │   ├── svm.yaml
   │   │   ├── logistic_regression.yaml
   │   │   └── gradient_boosting.yaml
   │   ├── training/
   │   │   └── default.yaml         # Training settings
   │   └── evaluation/
   │       └── classification.yaml  # Evaluation settings
   └── clearml/
       └── config.yaml              # ClearML settings

Main Configuration File
-----------------------

The main configuration file (``config/config.yaml``) defines the overall experiment setup:

.. code-block:: yaml

   # Default experiment settings
   defaults:
     - _self_
     - data: iris
     - model: random_forest
     - training: default
     - evaluation: classification

   # Experiment metadata
   experiment:
     name: "iris_classification"
     description: "Iris flower classification experiment"
     tags: ["iris", "classification", "tutorial"]

   # Global settings
   random_seed: 42
   verbose: true

   # Output directories
   output_dir: "./outputs"
   model_dir: "./models"
   report_dir: "./reports"

Data Configuration
------------------

Dataset settings are defined in ``config/hydra/data/iris.yaml``:

.. code-block:: yaml

   # Dataset configuration
   name: "iris"
   source: "sklearn"  # or "csv" for custom data
   target_column: "species"

   # Data splitting
   test_size: 0.2
   val_size: 0.1
   random_state: 42

   # Preprocessing
   preprocessing:
     scale_features: true
     scaler_type: "standard"  # standard, minmax, robust
     handle_missing: "drop"   # drop, mean, median

   # Feature engineering
   features:
     add_polynomial: false
     polynomial_degree: 2
     add_interactions: false

Model Configurations
--------------------

Each model has its own configuration file with hyperparameters:

**Random Forest (``config/hydra/model/random_forest.yaml``):**

.. code-block:: yaml

   name: "random_forest"
   type: "sklearn.ensemble.RandomForestClassifier"

   parameters:
     n_estimators: 100
     max_depth: null
     min_samples_split: 2
     min_samples_leaf: 1
     max_features: "sqrt"
     bootstrap: true
     random_state: 42

**SVM (``config/hydra/model/svm.yaml``):**

.. code-block:: yaml

   name: "svm"
   type: "sklearn.svm.SVC"

   parameters:
     C: 1.0
     kernel: "rbf"
     gamma: "scale"
     probability: true
     random_state: 42

**Logistic Regression (``config/hydra/model/logistic_regression.yaml``):**

.. code-block:: yaml

   name: "logistic_regression"
   type: "sklearn.linear_model.LogisticRegression"

   parameters:
     C: 1.0
     penalty: "l2"
     solver: "lbfgs"
     max_iter: 1000
     random_state: 42

**Gradient Boosting (``config/hydra/model/gradient_boosting.yaml``):**

.. code-block:: yaml

   name: "gradient_boosting"
   type: "sklearn.ensemble.GradientBoostingClassifier"

   parameters:
     n_estimators: 100
     learning_rate: 0.1
     max_depth: 3
     min_samples_split: 2
     min_samples_leaf: 1
     subsample: 1.0
     random_state: 42

Training Configuration
----------------------

Training settings are defined in ``config/hydra/training/default.yaml``:

.. code-block:: yaml

   # Training parameters
   epochs: 100
   batch_size: 32
   learning_rate: 0.001

   # Cross-validation
   cv_folds: 5
   cv_scoring: "accuracy"

   # Early stopping
   early_stopping:
     enabled: false
     patience: 10
     min_delta: 0.001

   # Model checkpointing
   checkpoint:
     enabled: true
     save_best_only: true
     monitor: "val_accuracy"

Evaluation Configuration
-------------------------

Evaluation settings are defined in ``config/hydra/evaluation/classification.yaml``:

.. code-block:: yaml

   # Evaluation metrics
   metrics:
     - "accuracy"
     - "precision_macro"
     - "recall_macro"
     - "f1_macro"
     - "roc_auc_ovr"

   # Classification-specific settings
   classification:
     average: "macro"
     multiclass_strategy: "ovr"

   # Report generation
   reports:
     confusion_matrix: true
     classification_report: true
     feature_importance: true
     learning_curves: false

   # Visualization
   plots:
     confusion_matrix: true
     roc_curves: true
     precision_recall_curves: false
     feature_importance: true

Using Configurations
--------------------

Command Line Override
~~~~~~~~~~~~~~~~~~~~~

Override configuration values from the command line:

.. code-block:: bash

   # Override model parameters
   python src/run.py model=random_forest model.parameters.n_estimators=200

   # Change dataset settings
   python src/run.py data.test_size=0.3

   # Modify training settings
   python src/run.py training.cv_folds=10

Configuration Groups
~~~~~~~~~~~~~~~~~~~~

Use different configuration groups:

.. code-block:: bash

   # Use different model
   python src/run.py +model=svm

   # Use different data configuration
   python src/run.py +data=custom_dataset

   # Combine different configs
   python src/run.py +model=gradient_boosting +training=extended

Configuration Composition
~~~~~~~~~~~~~~~~~~~~~~~~~

Create composite configurations using ``config/composed/`` files:

.. code-block:: yaml

   # Example: iris_random_forest.yaml
   defaults:
     - _self_
     - /data: iris
     - /model: random_forest
     - /training: default
     - /evaluation: classification

   # Custom overrides
   model:
     parameters:
       n_estimators: 150
       max_depth: 10

Environment Variables
---------------------

Configure the project using environment variables:

.. code-block:: bash

   # Set experiment name
   export EXPERIMENT_NAME="my_custom_experiment"

   # Configure MLflow
   export MLFLOW_TRACKING_URI="http://localhost:5000"

   # Set ClearML credentials
   export CLEARML_API_ACCESS_KEY="your_key"
   export CLEARML_API_SECRET_KEY="your_secret"

   # Set random seed
   export RANDOM_SEED=123

Configuration Validation
------------------------

The project includes configuration validation:

.. code-block:: python

   from src.config import validate_config
   from omegaconf import OmegaConf

   # Load and validate configuration
   cfg = OmegaConf.load("config/config.yaml")
   validated_cfg = validate_config(cfg)

   print("Configuration is valid!")

Configuration Examples
----------------------

Basic Classification Experiment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python src/run.py \
     experiment.name="basic_rf_experiment" \
     model=random_forest \
     model.parameters.n_estimators=100 \
     data.test_size=0.2

Hyperparameter Sweep
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Random Forest hyperparameter sweep
   python src/run.py \
     model=random_forest \
     model.parameters.n_estimators=50,100,200 \
     model.parameters.max_depth=5,10,null \
     training.cv_folds=5

Cross-Validation Experiment
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python src/run.py \
     training.cv_folds=10 \
     training.cv_scoring="f1_macro" \
     evaluation.reports.learning_curves=true

Multi-Model Comparison
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Compare multiple models
   python scripts/compare_experiments.py \
     --models random_forest svm logistic_regression gradient_boosting \
     --output reports/model_comparison.md

Custom Model Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a custom model configuration:

.. code-block:: yaml

   # config/hydra/model/custom_model.yaml
   name: "custom_model"
   type: "src.models.custom_model.CustomClassifier"

   parameters:
     custom_param1: 1.0
     custom_param2: "value"

Then use it:

.. code-block:: bash

   python src/run.py +model=custom_model

Advanced Configuration
----------------------

Hierarchical Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use hierarchical overrides:

.. code-block:: bash

   python src/run.py \
     ~model.parameters \
     +model.parameters.custom_param=42 \
     ++model.parameters.another_param="test"

Configuration Merging
~~~~~~~~~~~~~~~~~~~~~

Merge configurations from multiple sources:

.. code-block:: python

   from omegaconf import OmegaConf, DictConfig

   # Load base config
   base_cfg = OmegaConf.load("config/config.yaml")

   # Load override config
   override_cfg = OmegaConf.load("config/overrides.yaml")

   # Merge configurations
   final_cfg = OmegaConf.merge(base_cfg, override_cfg)

Dynamic Configuration
~~~~~~~~~~~~~~~~~~~~~

Create dynamic configurations based on conditions:

.. code-block:: python

   def create_dynamic_config(model_type: str) -> DictConfig:
       """Create configuration based on model type."""
       base_config = {
           "experiment": {"name": f"{model_type}_experiment"},
           "model": model_type,
       }

       if model_type == "random_forest":
           base_config["model.parameters"] = {
               "n_estimators": 100,
               "max_depth": 10
           }
       elif model_type == "svm":
           base_config["model.parameters"] = {
               "C": 1.0,
               "kernel": "rbf"
           }

       return OmegaConf.create(base_config)

Configuration Best Practices
----------------------------

1. **Use Descriptive Names**: Give configurations clear, descriptive names
2. **Document Parameters**: Add comments explaining parameter purposes
3. **Version Control**: Keep configuration files under version control
4. **Validation**: Always validate configurations before running experiments
5. **Modularity**: Split configurations into logical, reusable components
6. **Environment Separation**: Use different configs for development/production

Troubleshooting
---------------

**Configuration Not Found:**

.. code-block:: bash

   # Check if config file exists
   ls config/hydra/model/

   # Validate YAML syntax
   python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"

**Parameter Override Issues:**

.. code-block:: bash

   # Use quotes for string values
   python src/run.py model.parameters.kernel="linear"

   # Use proper dot notation
   python src/run.py model.random_forest.n_estimators=200

**Configuration Conflicts:**

Check for conflicting parameter definitions in configuration files and command line overrides.
