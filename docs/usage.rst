Usage Guide
===========

This guide provides comprehensive examples of how to use the Iris Data Science Project for various machine learning tasks.

Basic Usage Patterns
--------------------

Training a Single Model
~~~~~~~~~~~~~~~~~~~~~~~

The simplest way to train a model:

.. code-block:: python

   from src.models.train_model import train_model
   from sklearn.datasets import load_iris

   # Load data
   iris = load_iris()
   X, y = iris.data, iris.target

   # Train a random forest model
   model = train_model(X, y, model_type='random_forest')
   print(f"Model trained with accuracy: {model.score(X, y):.3f}")

Using Configuration Files
~~~~~~~~~~~~~~~~~~~~~~~~~

For more complex scenarios, use Hydra configurations:

.. code-block:: python

   import hydra
   from omegaconf import DictConfig
   from src.run import run_experiment

   @hydra.main(config_path="../config/hydra", config_name="config", version_base=None)
   def main(cfg: DictConfig):
       run_experiment(cfg)

   if __name__ == "__main__":
       main()

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

Use the command line interface for quick experiments:

.. code-block:: bash

   # Train with default settings
   python src/run.py experiment=random_forest

   # Train with custom parameters
   python src/run.py experiment=svm kernel=rbf C=1.0

   # Use cross-validation
   python scripts/cross_validation.py --model random_forest --folds 5

Experiment Tracking
-------------------

MLflow Integration
~~~~~~~~~~~~~~~~~~

Automatically track experiments with MLflow:

.. code-block:: python

   import mlflow
   import mlflow.sklearn
   from src.models.mlflow_utils import setup_mlflow_experiment

   # Set up experiment
   setup_mlflow_experiment("iris_classification")

   with mlflow.start_run():
       # Your training code here
       model = train_model(X, y, model_type='random_forest')

       # Log parameters
       mlflow.log_param("model_type", "random_forest")
       mlflow.log_param("n_estimators", 100)

       # Log metrics
       accuracy = model.score(X, y)
       mlflow.log_metric("accuracy", accuracy)

       # Log model
       mlflow.sklearn.log_model(model, "model")

ClearML Integration
~~~~~~~~~~~~~~~~~~~

Track experiments with ClearML:

.. code-block:: python

   from clearml import Task
   from src.models.clearml_pipeline import create_clearml_task

   # Create task
   task = create_clearml_task("iris_experiment")

   # Your experiment code here
   model = train_model(X, y, model_type='gradient_boosting')

   # Log artifacts
   task.upload_artifact("trained_model", model)

Data Pipeline Examples
----------------------

Data Loading and Preprocessing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from src.data.make_dataset import load_iris_data, preprocess_data

   # Load raw data
   data = load_iris_data()

   # Preprocess data
   X_train, X_test, y_train, y_test = preprocess_data(data)

   print(f"Training set shape: {X_train.shape}")
   print(f"Test set shape: {X_test.shape}")

Feature Engineering
~~~~~~~~~~~~~~~~~~~

Add custom features to the dataset:

.. code-block:: python

   import numpy as np
   from sklearn.preprocessing import StandardScaler

   def add_features(X):
       """Add engineered features to the dataset."""
       # Add polynomial features
       X_poly = np.column_stack([
           X,
           X[:, 0] * X[:, 1],  # sepal length * sepal width
           X[:, 2] * X[:, 3],  # petal length * petal width
           X[:, 0] / (X[:, 1] + 0.1),  # sepal length / sepal width
       ])

       # Scale features
       scaler = StandardScaler()
       X_scaled = scaler.fit_transform(X_poly)

       return X_scaled

   # Apply feature engineering
   X_train_featured = add_features(X_train)
   X_test_featured = add_features(X_test)

Model Training Examples
-----------------------

Comparing Multiple Models
~~~~~~~~~~~~~~~~~~~~~~~~~

Train and compare different algorithms:

.. code-block:: python

   from src.models.compare_experiments import compare_models
   from sklearn.model_selection import train_test_split

   # Split data
   X_train, X_test, y_train, y_test = train_test_split(
       X, y, test_size=0.2, random_state=42
   )

   # Define models to compare
   models = ['random_forest', 'svm', 'logistic_regression', 'gradient_boosting']

   # Compare models
   results = compare_models(X_train, y_train, models)

   # Print results
   for model_name, metrics in results.items():
       print(f"{model_name}: Accuracy = {metrics['accuracy']:.3f}")

Hyperparameter Tuning
~~~~~~~~~~~~~~~~~~~~~

Perform hyperparameter optimization:

.. code-block:: python

   from sklearn.model_selection import GridSearchCV
   from sklearn.ensemble import RandomForestClassifier

   # Define parameter grid
   param_grid = {
       'n_estimators': [50, 100, 200],
       'max_depth': [None, 10, 20],
       'min_samples_split': [2, 5, 10]
   }

   # Create model
   rf = RandomForestClassifier(random_state=42)

   # Perform grid search
   grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='accuracy')
   grid_search.fit(X_train, y_train)

   print(f"Best parameters: {grid_search.best_params_}")
   print(f"Best score: {grid_search.best_score_:.3f}")

Cross-Validation
~~~~~~~~~~~~~~~~

Use cross-validation for robust evaluation:

.. code-block:: python

   from sklearn.model_selection import cross_val_score
   from sklearn.ensemble import GradientBoostingClassifier

   # Create model
   gb = GradientBoostingClassifier(n_estimators=100, random_state=42)

   # Perform cross-validation
   scores = cross_val_score(gb, X, y, cv=5, scoring='accuracy')

   print(f"Cross-validation scores: {scores}")
   print(f"Mean accuracy: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")

Model Evaluation
----------------

Comprehensive Evaluation
~~~~~~~~~~~~~~~~~~~~~~~~

Evaluate model performance with multiple metrics:

.. code-block:: python

   from sklearn.metrics import classification_report, confusion_matrix
   from src.models.train_model import evaluate_model

   # Train model
   model = train_model(X_train, y_train, model_type='random_forest')

   # Evaluate
   metrics = evaluate_model(model, X_test, y_test)

   print("Classification Report:")
   print(classification_report(y_test, metrics['predictions']))

   print("Confusion Matrix:")
   print(confusion_matrix(y_test, metrics['predictions']))

Visualization Examples
----------------------

Plotting Results
~~~~~~~~~~~~~~~~

Create visualizations of model performance:

.. code-block:: python

   import matplotlib.pyplot as plt
   import seaborn as sns
   from src.visualization.visualize import plot_confusion_matrix, plot_feature_importance

   # Set style
   sns.set_style("whitegrid")

   # Plot confusion matrix
   plt.figure(figsize=(8, 6))
   plot_confusion_matrix(y_test, predictions, class_names=['setosa', 'versicolor', 'virginica'])
   plt.title("Confusion Matrix")
   plt.show()

   # Plot feature importance (for tree-based models)
   if hasattr(model, 'feature_importances_'):
       plt.figure(figsize=(10, 6))
       plot_feature_importance(model, feature_names=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])
       plt.title("Feature Importance")
       plt.show()

Workflow Orchestration
----------------------

Using Snakemake
~~~~~~~~~~~~~~~

Run the complete pipeline with Snakemake:

.. code-block:: bash

   # Run the entire workflow
   snakemake

   # Run specific rules
   snakemake train_models
   snakemake evaluate_models

   # Run with different configuration
   snakemake --config model=random_forest

Using Make
~~~~~~~~~~

Use the Makefile for common tasks:

.. code-block:: bash

   # Run complete pipeline
   make all

   # Individual steps
   make data
   make train
   make evaluate
   make report

   # Clean up
   make clean

Advanced Usage
--------------

Custom Model Classes
~~~~~~~~~~~~~~~~~~~~

Implement your own model classes:

.. code-block:: python

   from sklearn.base import BaseEstimator, ClassifierMixin
   from sklearn.utils.validation import check_X_y, check_array
   import numpy as np

   class CustomClassifier(BaseEstimator, ClassifierMixin):
       """Custom classifier example."""

       def __init__(self, custom_param=1.0):
           self.custom_param = custom_param

       def fit(self, X, y):
           X, y = check_X_y(X, y)
           self.classes_ = np.unique(y)
           # Your fitting logic here
           return self

       def predict(self, X):
           X = check_array(X)
           # Your prediction logic here
           return np.zeros(X.shape[0])  # Placeholder

Pipeline Integration
~~~~~~~~~~~~~~~~~~~~

Create complex pipelines:

.. code-block:: python

   from sklearn.pipeline import Pipeline
   from sklearn.preprocessing import StandardScaler
   from sklearn.decomposition import PCA
   from sklearn.ensemble import RandomForestClassifier

   # Create pipeline
   pipeline = Pipeline([
       ('scaler', StandardScaler()),
       ('pca', PCA(n_components=2)),
       ('classifier', RandomForestClassifier(n_estimators=100))
   ])

   # Train pipeline
   pipeline.fit(X_train, y_train)

   # Evaluate
   accuracy = pipeline.score(X_test, y_test)
   print(f"Pipeline accuracy: {accuracy:.3f}")

Error Handling
~~~~~~~~~~~~~~

Robust error handling in your experiments:

.. code-block:: python

   from src.models.pipeline_monitor import PipelineMonitor

   # Create monitor
   monitor = PipelineMonitor()

   try:
       # Your experiment code here
       with monitor.track_experiment("my_experiment"):
           model = train_model(X, y, model_type='random_forest')

           # Log success
           monitor.log_success("Model training completed")

   except Exception as e:
       # Log error
       monitor.log_error(f"Experiment failed: {str(e)}")
       raise

Performance Monitoring
~~~~~~~~~~~~~~~~~~~~~~

Monitor model performance over time:

.. code-block:: python

   from src.models.pipeline_monitor import monitor_model_performance

   # Monitor model performance
   performance_report = monitor_model_performance(model, X_test, y_test)

   # Check for performance degradation
   if performance_report['accuracy'] < 0.8:
       print("WARNING: Model performance degraded!")

   # Log performance metrics
   monitor.log_metrics(performance_report)
