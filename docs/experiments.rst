Experiments Guide
================

This guide explains how to design, run, and analyze machine learning experiments in the Iris Data Science Project.

Experiment Planning
-------------------

Before running experiments, plan your approach:

1. **Define Objectives**: What are you trying to achieve?
2. **Select Metrics**: Choose appropriate evaluation metrics
3. **Design Experiments**: Plan your experimental setup
4. **Set Baselines**: Establish baseline performance
5. **Plan Analysis**: Decide how you'll analyze results

Experiment Types
-----------------

Basic Model Training
~~~~~~~~~~~~~~~~~~~~

Train a single model with default settings:

.. code-block:: bash

   # Train Random Forest
   python src/run.py experiment.name="rf_baseline" model=random_forest

   # Train SVM
   python src/run.py experiment.name="svm_baseline" model=svm

   # Train Logistic Regression
   python src/run.py experiment.name="lr_baseline" model=logistic_regression

Hyperparameter Tuning
~~~~~~~~~~~~~~~~~~~~~

Optimize model hyperparameters:

.. code-block:: bash

   # Random Forest tuning
   python src/run.py \
     experiment.name="rf_tuning" \
     model=random_forest \
     model.parameters.n_estimators=50,100,200 \
     model.parameters.max_depth=5,10,15,null

   # SVM tuning
   python src/run.py \
     experiment.name="svm_tuning" \
     model=svm \
     model.parameters.C=0.1,1.0,10.0 \
     model.parameters.kernel=rbf,linear

Cross-Validation Experiments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use cross-validation for robust evaluation:

.. code-block:: bash

   # 10-fold cross-validation
   python src/run.py \
     experiment.name="cv_experiment" \
     training.cv_folds=10 \
     training.cv_scoring=accuracy,f1_macro,precision_macro,recall_macro

Multi-Model Comparison
~~~~~~~~~~~~~~~~~~~~~~~

Compare multiple models simultaneously:

.. code-block:: bash

   # Use the comparison script
   python scripts/compare_experiments.py \
     --models random_forest svm logistic_regression gradient_boosting \
     --cv-folds 5 \
     --output reports/model_comparison.json

Ablation Studies
~~~~~~~~~~~~~~~~

Test the impact of different features or components:

.. code-block:: bash

   # Experiment with feature scaling
   python src/run.py \
     experiment.name="no_scaling" \
     data.preprocessing.scale_features=false

   python src/run.py \
     experiment.name="with_scaling" \
     data.preprocessing.scale_features=true

Data Size Experiments
~~~~~~~~~~~~~~~~~~~~~

Test performance with different dataset sizes:

.. code-block:: bash

   # Small dataset
   python src/run.py \
     experiment.name="small_data" \
     data.test_size=0.8

   # Large dataset (if available)
   python src/run.py \
     experiment.name="large_data" \
     data.test_size=0.1

Running Experiments
-------------------

Using the Command Line
~~~~~~~~~~~~~~~~~~~~~~~

Basic experiment execution:

.. code-block:: bash

   # Run single experiment
   python src/run.py experiment.name="my_experiment"

   # Run with custom configuration
   python src/run.py \
     experiment.name="custom_experiment" \
     model=gradient_boosting \
     model.parameters.n_estimators=200 \
     training.cv_folds=5

Using Snakemake
~~~~~~~~~~~~~~~

Run experiments with workflow orchestration:

.. code-block:: bash

   # Run all experiments
   snakemake all_experiments

   # Run specific experiment type
   snakemake experiment_random_forest

   # Run with different configuration
   snakemake --config model=svm experiment_svm

Using Make
~~~~~~~~~~

Use the Makefile for common experiment patterns:

.. code-block:: bash

   # Run all experiments
   make experiments

   # Run hyperparameter tuning
   make tune

   # Run cross-validation
   make cv

Batch Experiments
~~~~~~~~~~~~~~~~~

Run multiple experiments in batch:

.. code-block:: bash

   # Create experiment script
   cat > run_experiments.sh << 'EOF'
   #!/bin/bash
   models=("random_forest" "svm" "logistic_regression" "gradient_boosting")

   for model in "${models[@]}"; do
       echo "Running experiment for $model"
       python src/run.py \
         experiment.name="${model}_experiment" \
         model="$model" \
         training.cv_folds=5
   done
   EOF

   # Make executable and run
   chmod +x run_experiments.sh
   ./run_experiments.sh

Automated Experimentation
~~~~~~~~~~~~~~~~~~~~~~~~~

Set up automated experiment runs:

.. code-block:: bash

   # Schedule experiments with cron
   echo "0 */4 * * * cd /path/to/project && make experiments" | crontab -

   # Or use CI/CD pipeline for automated experiments
   # See .github/workflows/experiments.yml

Experiment Tracking
-------------------

MLflow Integration
~~~~~~~~~~~~~~~~~~

Track experiments with MLflow:

.. code-block:: python

   import mlflow
   from src.models.mlflow_utils import setup_experiment

   # Set up experiment
   setup_experiment("iris_experiments")

   # Run experiments (automatically tracked)
   python src/run.py experiment.name="tracked_experiment"

   # View results
   mlflow ui

ClearML Integration
~~~~~~~~~~~~~~~~~~~

Track experiments with ClearML:

.. code-block:: python

   from clearml import Task
   from src.models.clearml_pipeline import create_experiment_task

   # Create task
   task = create_experiment_task("iris_experiment")

   # Run experiment
   python src/run.py experiment.name="clearml_experiment"

   # View on ClearML web UI
   # https://app.clear.ml

Experiment Analysis
-------------------

Performance Metrics
~~~~~~~~~~~~~~~~~~~

Analyze model performance:

.. code-block:: python

   from src.models.compare_experiments import load_experiment_results
   import pandas as pd

   # Load results
   results = load_experiment_results("reports/experiment_results.json")

   # Create comparison table
   df = pd.DataFrame(results)
   print(df[['model', 'accuracy', 'f1_score', 'training_time']].sort_values('accuracy', ascending=False))

Statistical Significance
~~~~~~~~~~~~~~~~~~~~~~~~

Test for statistical significance:

.. code-block:: python

   from scipy import stats
   import numpy as np

   # Load cross-validation scores
   rf_scores = np.array([0.95, 0.93, 0.96, 0.94, 0.95])
   svm_scores = np.array([0.92, 0.91, 0.93, 0.90, 0.92])

   # Perform t-test
   t_stat, p_value = stats.ttest_ind(rf_scores, svm_scores)

   print(f"T-statistic: {t_stat:.3f}")
   print(f"P-value: {p_value:.3f}")
   print("Significant difference!" if p_value < 0.05 else "No significant difference")

Error Analysis
~~~~~~~~~~~~~~

Analyze model errors:

.. code-block:: python

   from sklearn.metrics import confusion_matrix
   import seaborn as sns
   import matplotlib.pyplot as plt

   # Load predictions and true labels
   y_true, y_pred = load_predictions("results/latest_experiment/")

   # Create confusion matrix
   cm = confusion_matrix(y_true, y_pred)
   labels = ['setosa', 'versicolor', 'virginica']

   # Plot
   plt.figure(figsize=(8, 6))
   sns.heatmap(cm, annot=True, fmt='d', xticklabels=labels, yticklabels=labels)
   plt.title("Confusion Matrix")
   plt.show()

Feature Importance
~~~~~~~~~~~~~~~~~~

Analyze feature importance:

.. code-block:: python

   from src.visualization.visualize import plot_feature_importance

   # For tree-based models
   model = load_model("models/random_forest.pkl")
   feature_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']

   plot_feature_importance(model, feature_names)
   plt.show()

Learning Curves
~~~~~~~~~~~~~~~

Analyze learning behavior:

.. code-block:: python

   from sklearn.model_selection import learning_curve
   import matplotlib.pyplot as plt

   # Generate learning curve
   train_sizes, train_scores, val_scores = learning_curve(
       model, X, y, cv=5, scoring='accuracy',
       train_sizes=np.linspace(0.1, 1.0, 10)
   )

   # Plot
   plt.figure(figsize=(10, 6))
   plt.plot(train_sizes, np.mean(train_scores, axis=1), label='Training score')
   plt.plot(train_sizes, np.mean(val_scores, axis=1), label='Validation score')
   plt.xlabel('Training set size')
   plt.ylabel('Accuracy')
   plt.legend()
   plt.show()

Experiment Reporting
--------------------

Automated Reports
~~~~~~~~~~~~~~~~~

Generate comprehensive reports:

.. code-block:: bash

   # Generate experiment report
   python scripts/generate_report.py \
     --experiment "my_experiment" \
     --output reports/experiment_report.md

   # Generate comparison report
   python scripts/generate_report.py \
     --compare "experiment1,experiment2,experiment3" \
     --output reports/comparison_report.md

Custom Reports
~~~~~~~~~~~~~~

Create custom analysis reports:

.. code-block:: python

   from src.models.experiment_analyzer import ExperimentAnalyzer

   # Create analyzer
   analyzer = ExperimentAnalyzer()

   # Analyze experiments
   report = analyzer.analyze_experiments([
       "rf_baseline",
       "svm_baseline",
       "lr_baseline"
   ])

   # Generate report
   analyzer.generate_report(report, "reports/custom_analysis.md")

Experiment Reproducibility
---------------------------

Seed Management
~~~~~~~~~~~~~~~

Ensure reproducible results:

.. code-block:: bash

   # Set fixed random seed
   python src/run.py random_seed=42

   # Or set environment variable
   export RANDOM_SEED=42
   python src/run.py

Version Control
~~~~~~~~~~~~~~~

Track code and data versions:

.. code-block:: bash

   # Track data version
   dvc add data/processed/
   dvc commit

   # Track code version
   git add .
   git commit -m "Experiment: baseline models"

Environment Snapshot
~~~~~~~~~~~~~~~~~~~~

Save environment state:

.. code-block:: bash

   # Save conda environment
   conda env export > environment.yml

   # Save pip requirements
   pip freeze > requirements.txt

   # Save system information
   python scripts/check_health.py --save system_info.json

Experiment Best Practices
-------------------------

1. **Naming Conventions**: Use descriptive experiment names
2. **Version Control**: Track all code and configuration changes
3. **Documentation**: Document experiment objectives and setup
4. **Reproducibility**: Set random seeds and save environment state
5. **Modular Design**: Keep experiments focused on single objectives
6. **Result Backup**: Save results to persistent storage
7. **Error Handling**: Implement proper error handling and logging

Common Experiment Patterns
--------------------------

Baseline Establishment
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Establish baselines for all models
   for model in random_forest svm logistic_regression gradient_boosting; do
       python src/run.py \
         experiment.name="${model}_baseline" \
         model="$model" \
         training.cv_folds=5
   done

Incremental Improvement
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Start with baseline
   python src/run.py experiment.name="v1_baseline"

   # Add feature engineering
   python src/run.py experiment.name="v2_features" data.features.add_polynomial=true

   # Tune hyperparameters
   python src/run.py experiment.name="v3_tuned" model.parameters.n_estimators=200

   # Try ensemble
   python src/run.py experiment.name="v4_ensemble" model=gradient_boosting

Hyperparameter Optimization
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from sklearn.model_selection import RandomizedSearchCV
   from scipy.stats import randint, uniform

   # Define parameter distributions
   param_dist = {
       'n_estimators': randint(50, 200),
       'max_depth': randint(3, 10),
       'min_samples_split': randint(2, 10)
   }

   # Perform random search
   random_search = RandomizedSearchCV(
       RandomForestClassifier(),
       param_dist,
       n_iter=20,
       cv=5,
       scoring='accuracy'
   )

   random_search.fit(X_train, y_train)
   print(f"Best parameters: {random_search.best_params_}")

Model Selection Pipeline
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 1. Quick comparison with default parameters
   make quick_compare

   # 2. Hyperparameter tuning for top performers
   make tune_top_models

   # 3. Cross-validation with best parameters
   make final_cv

   # 4. Generate final report
   make final_report

Troubleshooting Experiments
----------------------------

**Inconsistent Results:**

.. code-block:: bash

   # Check random seed
   python src/run.py random_seed=42 --debug

   # Verify data splitting
   python scripts/validate_data.py

**Memory Issues:**

.. code-block:: bash

   # Reduce batch size
   python src/run.py training.batch_size=16

   # Use smaller models
   python src/run.py model.parameters.n_estimators=50

**Long Training Times:**

.. code-block:: bash

   # Enable early stopping
   python src/run.py training.early_stopping.enabled=true

   # Reduce cross-validation folds
   python src/run.py training.cv_folds=3

**Experiment Tracking Issues:**

.. code-block:: bash

   # Check MLflow server
   curl http://localhost:5000/health

   # Verify ClearML configuration
   clearml-task --help
