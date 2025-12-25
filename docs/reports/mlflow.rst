MLflow Experiment Tracking Report
================================

.. include:: ../../reports/MLflow_Experiment_Tracking_Report.md
   :parser: myst_parser.sphinx_

Additional Analysis
-------------------

Experiment Performance Visualization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import matplotlib.pyplot as plt
   import seaborn as sns
   from mlflow.tracking import MlflowClient

   # Connect to MLflow
   client = MlflowClient()

   # Get experiment data
   experiment = client.get_experiment_by_name("iris_ml_experiments")
   runs = client.search_runs([experiment.experiment_id])

   # Extract metrics
   accuracies = [run.data.metrics.get('accuracy', 0) for run in runs]
   models = [run.data.tags.get('model_type', 'unknown') for run in runs]

   # Create visualization
   plt.figure(figsize=(12, 6))
   sns.boxplot(x=models, y=accuracies)
   plt.title('Model Accuracy Distribution')
   plt.xticks(rotation=45)
   plt.tight_layout()
   plt.show()

Key Insights
~~~~~~~~~~~~

From the MLflow experiments, several important insights emerge:

1. **Linear Models Excellence**: SVM with linear kernel and L2-regularized Logistic Regression achieved perfect classification (100% accuracy)

2. **Ensemble Robustness**: Tree-based ensemble methods (Random Forest, Gradient Boosting) consistently performed well across different configurations

3. **Hyperparameter Sensitivity**: Some models showed significant performance variations with parameter tuning, while others were relatively stable

4. **Computational Trade-offs**: More complex models generally required more computation time but didn't always yield proportional accuracy gains

Best Practices Learned
~~~~~~~~~~~~~~~~~~~~~~

* Always log comprehensive metrics, not just accuracy
* Use cross-validation for robust performance estimation
* Track computational resources (time, memory)
* Implement proper model serialization with signatures
* Maintain clear experiment naming conventions

Experiment Comparison Table
~~~~~~~~~~~~~~~~~~~~~~~~~~~

+--------------------+----------+----------+-----------+--------+-------------+
| Model              | Accuracy | F1 Score | Precision | Recall | Training Time|
+====================+==========+==========+===========+========+=============+
| SVM_Linear         | 1.0000   | 1.0000   | 1.0000    | 1.0000 | 0.02s       |
+--------------------+----------+----------+-----------+--------+-------------+
| LogisticRegression | 1.0000   | 1.0000   | 1.0000    | 1.0000 | 0.01s       |
+--------------------+----------+----------+-----------+--------+-------------+
| RandomForest       | 0.9667   | 0.9666   | 0.9697    | 0.9667 | 0.15s       |
+--------------------+----------+----------+-----------+--------+-------------+
| GradientBoosting   | 0.9667   | 0.9666   | 0.9697    | 0.9667 | 0.08s       |
+--------------------+----------+----------+-----------+--------+-------------+
| SVM_RBF            | 0.9667   | 0.9666   | 0.9697    | 0.9667 | 0.03s       |
+--------------------+----------+----------+-----------+--------+-------------+
| DecisionTree       | 0.9667   | 0.9666   | 0.9697    | 0.9667 | 0.01s       |
+--------------------+----------+----------+-----------+--------+-------------+

Recommendations
~~~~~~~~~~~~~~~

Based on the experimental results:

1. **For Production Use**: SVM_Linear or LogisticRegression_L2 for their perfect performance and computational efficiency

2. **For Robustness**: Ensemble methods like RandomForest for consistent performance across different scenarios

3. **For Interpretability**: DecisionTree or LogisticRegression when model explainability is crucial

4. **For Scalability**: Consider training time and computational requirements when deploying at scale

Reproducibility
~~~~~~~~~~~~~~~

All experiments can be reproduced using:

.. code-block:: bash

   # Navigate to the project directory
   cd iris-data-science-project

   # Run MLflow experiments
   python src/models/run_experiments.py

   # View results in MLflow UI
   mlflow ui --backend-store-uri sqlite:///models/mlruns/mlflow.db

Future Work
~~~~~~~~~~~

Potential areas for further investigation:

* **Feature Engineering**: Test polynomial features, interactions, and domain-specific transformations
* **Advanced Algorithms**: Try XGBoost, LightGBM, or neural network architectures
* **Ensemble Strategies**: Implement stacking, blending, or custom ensemble methods
* **Cross-Validation Strategies**: Test different CV schemes and nested CV for hyperparameter tuning
* **Performance Monitoring**: Set up automated performance tracking and model retraining pipelines
