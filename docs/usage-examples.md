# Usage Examples

This document provides practical examples of how to use the Iris Data Science Project for various machine learning tasks.

## Quick Start Examples

### 1. Basic Model Training

```python
from src.models.train_model import train_model
from src.models.predict_model import predict_model
from sklearn.datasets import load_iris
import pandas as pd

# Load the iris dataset
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = iris.target

# Train a model
model = train_model(X, y, model_type='logistic_regression')

# Make predictions
predictions = predict_model(model, X[:5])
print(predictions)
```

### 2. Running Multiple Experiments

```python
from src.models.run_experiments import run_experiment_comparison
from src.models.compare_experiments import compare_experiments

# Run comparison of multiple models
models_to_test = [
    'logistic_regression',
    'random_forest', 
    'svm_linear',
    'svm_rbf'
]

results = run_experiment_comparison(
    X_train, X_test, y_train, y_test,
    models=models_to_test
)

# Compare results
comparison = compare_experiments(results)
print(comparison)
```

### 3. Using MLflow for Tracking

```python
from src.models.mlflow_utils import setup_mlflow, log_model_run
import mlflow

# Setup MLflow
setup_mlflow()

# Log a model run
with mlflow.start_run():
    model = train_model(X, y, model_type='random_forest')
    
    # Log parameters
    mlflow.log_param('model_type', 'random_forest')
    mlflow.log_param('n_estimators', 100)
    
    # Log metrics
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric('accuracy', accuracy)
    
    # Log model
    log_model_run(model, 'iris_model')
```

## Advanced Usage Examples

### 4. ClearML Pipeline Integration

```python
from src.models.clearml_pipeline import create_clearml_pipeline

# Create a ClearML pipeline
pipeline = create_clearml_pipeline()

# Define pipeline steps
pipeline.add_step(
    name='data_preprocessing',
    function=preprocess_iris_data,
    parameters={'scaling_method': 'standard'}
)

pipeline.add_step(
    name='model_training', 
    function=train_with_clearml,
    parameters={'model_type': 'gradient_boosting'}
)

pipeline.add_step(
    name='model_evaluation',
    function=evaluate_with_clearml,
    parameters={'metrics': ['accuracy', 'f1_macro']}
)

# Execute pipeline
pipeline.execute()
```

### 5. Configuration-Based Model Training

```python
from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra

# Initialize Hydra
GlobalHydra.instance().clear()
initialize(config_path="../config", job_name="config_example")

# Compose configuration
config = compose(
    config_name="config.yaml",
    overrides=["model=random_forest", "training.epochs=100"]
)

# Train model with config
from src.run import run_training
model = run_training(config)
```

### 6. Batch Processing and Evaluation

```python
from src.models.run_experiments import batch_evaluate_models
import pandas as pd

# Load configuration for batch evaluation
config = {
    'models': {
        'logistic_regression': {
            'params': {'C': [0.1, 1.0, 10.0]},
            'model_class': 'sklearn.linear_model.LogisticRegression'
        },
        'random_forest': {
            'params': {'n_estimators': [50, 100, 200]},
            'model_class': 'sklearn.ensemble.RandomForestClassifier'
        }
    },
    'evaluation': {
        'cv_folds': 5,
        'metrics': ['accuracy', 'f1_macro', 'precision_macro']
    }
}

# Run batch evaluation
results = batch_evaluate_models(X, y, config)
```

## Data Pipeline Examples

### 7. Custom Data Processing

```python
from src.data.make_dataset import prepare_iris_dataset
from src.features.build_features import create_feature_engineering_pipeline

# Custom data preparation
def custom_preprocessing(X, y):
    # Add feature engineering
    features = create_feature_engineering_pipeline()
    X_engineered = features.fit_transform(X)
    
    # Prepare dataset
    dataset = prepare_iris_dataset(X_engineered, y)
    
    return dataset

# Use custom preprocessing
dataset = custom_preprocessing(X, y)
```

### 8. Cross-Validation with Multiple Strategies

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score
from src.models.train_model import get_model

# Different CV strategies
cv_strategies = {
    'stratified_kfold': StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    'repeated_stratified': StratifiedKFold(n_splits=5, n_repeats=10, random_state=42)
}

# Evaluate with different CV strategies
for strategy_name, cv in cv_strategies.items():
    model = get_model('random_forest')
    scores = cross_val_score(model, X, y, cv=cv, scoring='f1_macro')
    print(f"{strategy_name}: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
```

## Model Analysis Examples

### 9. Feature Importance Analysis

```python
import matplotlib.pyplot as plt
from src.models.train_model import train_model
from sklearn.inspection import permutation_importance

# Train model
model = train_model(X, y, model_type='random_forest')

# Feature importance
feature_importance = model.feature_importances_
feature_names = X.columns

# Plot feature importance
plt.figure(figsize=(10, 6))
indices = feature_importance.argsort()[::-1]
plt.bar(range(len(feature_importance)), feature_importance[indices])
plt.title('Feature Importance')
plt.xticks(range(len(feature_importance)), [feature_names[i] for i in indices], rotation=45)
plt.tight_layout()
plt.show()

# Permutation importance
perm_importance = permutation_importance(model, X_test, y_test, random_state=42)
```

### 10. Model Comparison and Selection

```python
from src.models.compare_experiments import create_model_comparison_report
import pandas as pd

# Train multiple models
models = {
    'logistic_regression': train_model(X, y, model_type='logistic_regression'),
    'random_forest': train_model(X, y, model_type='random_forest'),
    'svm_linear': train_model(X, y, model_type='svm_linear'),
    'svm_rbf': train_model(X, y, model_type='svm_rbf')
}

# Create comparison report
comparison_data = []
for name, model in models.items():
    predictions = model.predict(X_test)
    
    from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
    
    comparison_data.append({
        'model': name,
        'accuracy': accuracy_score(y_test, predictions),
        'f1_score': f1_score(y_test, predictions, average='macro'),
        'precision': precision_score(y_test, predictions, average='macro'),
        'recall': recall_score(y_test, predictions, average='macro')
    })

comparison_df = pd.DataFrame(comparison_data)
print(comparison_df)
```

## Deployment Examples

### 11. Model Serialization and Loading

```python
import pickle
from src.models.train_model import train_model

# Train and save model
model = train_model(X, y, model_type='logistic_regression')

# Save model
with open('iris_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Load model for prediction
with open('iris_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

# Make predictions with loaded model
predictions = loaded_model.predict(X_test)
```

### 12. API Integration Example

```python
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from src.models.train_model import train_model

# Initialize FastAPI
app = FastAPI(title="Iris Classification API")

# Train model on startup
model = train_model(X, y, model_type='logistic_regression')

# Request model
class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float  
    petal_length: float
    petal_width: float

@app.post("/predict")
def predict_iris(request: IrisRequest):
    # Convert request to array
    features = np.array([[
        request.sepal_length,
        request.sepal_width,
        request.petal_length,
        request.petal_width
    ]])
    
    # Make prediction
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    
    return {
        "prediction": int(prediction),
        "class": iris.target_names[prediction],
        "probability": probability.tolist()
    }

# Run with: uvicorn app.main:app --reload
```

## Monitoring Examples

### 13. Model Performance Monitoring

```python
from src.models.pipeline_monitor import setup_model_monitoring
from src.models.train_model import train_model

# Train initial model
model = train_model(X, y, model_type='logistic_regression')

# Setup monitoring
monitor = setup_model_monitoring(
    model=model,
    X_baseline=X,
    y_baseline=y,
    monitoring_threshold=0.95
)

# Simulate new data and monitor
new_data = generate_new_iris_data()  # Your data generation function
monitor.check_data_drift(new_data)
monitor.check_performance_degradation(new_data)
```

### 14. Automated Model Retraining

```python
from src.models.pipeline_monitor import setup_auto_retraining
from src.data.make_dataset import prepare_iris_dataset

# Setup automatic retraining
auto_retrain = setup_auto_retraining(
    model_type='logistic_regression',
    retrain_trigger='performance_degradation',
    performance_threshold=0.90,
    retrain_data_size=1000
)

# Start monitoring
auto_retrain.start_monitoring()

# The system will automatically retrain when performance drops below threshold
```

## Best Practices Examples

### 15. Reproducible Experiment Setup

```python
import random
import numpy as np
import torch
from src.run import run_experiment_with_tracking

# Set all random seeds for reproducibility
random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

# Run experiment with full tracking
experiment_config = {
    'model': 'random_forest',
    'data_split': 'stratified',
    'cv_folds': 5,
    'random_state': 42,
    'tracking': {
        'mlflow': True,
        'clearml': True,
        'local_logging': True
    }
}

results = run_experiment_with_tracking(experiment_config)
```

### 16. Configuration Management

```python
from hydra import compose, initialize
from hydra.core.global_hydra import GlobalHydra

# Multiple configuration examples
configs = [
    "model=logistic_regression,training.epochs=100",
    "model=random_forest,training.n_estimators=200", 
    "model=svm,training.kernel=rbf,training.C=1.0"
]

for config_str in configs:
    GlobalHydra.instance().clear()
    initialize(config_path="../config", job_name="batch_experiment")
    
    config = compose(config_name="config.yaml", overrides=[config_str])
    results = run_training(config)
    print(f"Config: {config_str}")
    print(f"Results: {results}")
```

## Common Patterns and Templates

### Template 1: New Model Integration

```python
from src.models.train_model import ModelTrainer
from sklearn.base import BaseEstimator, ClassifierMixin

class YourCustomModel(BaseEstimator, ClassifierMixin):
    def __init__(self, param1=1.0, param2=1.0):
        self.param1 = param1
        self.param2 = param2
    
    def fit(self, X, y):
        # Your fitting logic here
        self.model_ = YourActualModel(param1=self.param1, param2=self.param2)
        self.model_.fit(X, y)
        return self
    
    def predict(self, X):
        return self.model_.predict(X)

# Register with trainer
trainer = ModelTrainer()
trainer.register_model('your_custom_model', YourCustomModel)

# Use in experiments
results = trainer.train_and_evaluate(
    X, y, 
    model_name='your_custom_model',
    model_params={'param1': 1.0, 'param2': 2.0}
)
```

### Template 2: Custom Metric

```python
from sklearn.metrics import make_scorer
import numpy as np

def balanced_accuracy(y_true, y_pred):
    """Custom balanced accuracy metric"""
    from sklearn.metrics import recall_score
    return recall_score(y_true, y_pred, average='macro')

# Create scorer
balanced_acc_scorer = make_scorer(balanced_accuracy)

# Use in cross-validation
from sklearn.model_selection import cross_val_score
model = train_model(X, y, model_type='random_forest')
scores = cross_val_score(model, X, y, cv=5, scoring=balanced_acc_scorer)
```

## Error Handling Examples

### Template 3: Robust Training Loop

```python
from src.models.train_model import train_model_with_validation
from src.models.pipeline_monitor import validate_model_inputs

def robust_training_pipeline(X, y, model_type='logistic_regression'):
    try:
        # Validate inputs
        validate_model_inputs(X, y)
        
        # Train with validation
        model = train_model_with_validation(
            X, y, 
            model_type=model_type,
            validation_split=0.2,
            early_stopping=True
        )
        
        # Validate model
        assert hasattr(model, 'predict'), "Model must have predict method"
        
        return model
        
    except Exception as e:
        print(f"Training failed: {str(e)}")
        # Implement fallback strategy
        return train_fallback_model(X, y)

# Use robust training
model = robust_training_pipeline(X, y, model_type='random_forest')
```

These examples demonstrate the key functionality of the Iris Data Science Project. Each example can be adapted for specific use cases and extended with additional features as needed.

For more detailed examples and advanced usage patterns, refer to the API documentation and source code comments.
