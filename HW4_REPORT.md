# HW4: Automated ML Pipelines with Modern Orchestration Tools

## Overview

This homework implements automated machine learning pipelines using modern orchestration tools as specified in the requirements. The pipeline demonstrates the integration of **Snakemake** for workflow orchestration and **Hydra** for configuration management.

## Tools and Technologies Used

### Core Orchestration Tools
- **Snakemake**: Workflow management system for creating reproducible and scalable data analyses
- **Hydra**: Configuration management framework for handling complex configurations

### Supporting Technologies
- **Python**: Core programming language
- **scikit-learn**: Machine learning algorithms and evaluation metrics
- **pandas/numpy**: Data manipulation and processing
- **MLflow**: Experiment tracking and model management
- **DVC**: Data version control

## Pipeline Architecture

### Workflow Stages

1. **Configuration Validation** (`validate_config`)
   - Validates Hydra configuration files
   - Ensures all required parameters are present

2. **Configuration Composition** (`compose_config`)
   - Composes specific configurations for each algorithm-dataset combination
   - Merges base, dataset, and model configurations

3. **Data Acquisition** (`download_data`)
   - Downloads raw datasets (currently supports Iris dataset)
   - Handles different data sources

4. **Data Preprocessing** (`preprocess_data`)
   - Splits data into train/test sets
   - Applies necessary preprocessing steps
   - Generates metadata

5. **Model Training** (`train_model`)
   - Trains models with different algorithms
   - Supports parallel execution
   - Logs training parameters and results

6. **Model Evaluation** (`evaluate_model`)
   - Evaluates trained models on test data
   - Generates comprehensive metrics and reports
   - Creates confusion matrices and classification reports

7. **Cross-Validation** (`cross_validation`)
   - Performs k-fold cross-validation
   - Provides robust performance estimates

8. **Reporting** (`generate_pipeline_report`)
   - Generates comprehensive performance reports
   - Compares all models and algorithms

9. **Notifications** (`send_notifications`)
   - Sends completion notifications
   - Supports Slack integration

10. **Health Monitoring** (`check_pipeline_health`)
    - Validates pipeline integrity
    - Checks for missing files and corrupted data

## Configuration Management with Hydra

### Configuration Structure

```
config/
├── config.yaml              # Main configuration
├── hydra/
│   ├── config.yaml          # Hydra base configuration
│   ├── data/
│   │   └── iris.yaml        # Dataset-specific config
│   └── model/               # Algorithm-specific configs
│       ├── random_forest.yaml
│       ├── svm.yaml
│       ├── logistic_regression.yaml
│       └── gradient_boosting.yaml
└── composed/                # Generated composed configs
    ├── iris_random_forest.yaml
    ├── iris_svm.yaml
    └── ...
```

### Configuration Features

- **Hierarchical Configuration**: Supports configuration inheritance and overrides
- **Validation**: Automatic validation of configuration parameters
- **Composition**: Dynamic composition of configurations for different experiments
- **Type Safety**: Ensures configuration values have correct types

## Snakemake Workflow Orchestration

### Key Features

- **DAG-based Execution**: Automatic dependency resolution
- **Parallel Execution**: Supports multi-core and distributed execution
- **Caching**: Intelligent caching of intermediate results
- **Reproducibility**: Ensures reproducible execution
- **Scalability**: Scales from local execution to cluster environments

### Workflow Rules

```python
# Example rule structure
rule train_model:
    input:
        train="data/processed/{dataset}/train.csv",
        config="config/composed/{dataset}_{algorithm}.yaml"
    output:
        model="models/{dataset}/{algorithm}/model.pkl",
        params="models/{dataset}/{algorithm}/params.json",
        training_log="models/{dataset}/{algorithm}/training.log"
    threads: 4
    shell:
        "python scripts/train_model.py {params.dataset} {params.algorithm} {input.config}"
```

## Pipeline Execution

### Running the Pipeline

```bash
# Execute complete pipeline
snakemake --cores 4

# Execute specific rule
snakemake train_model --cores 4

# Dry run to check workflow
snakemake --dry-run --cores 1

# Clean intermediate files
snakemake clean
```

### Parallel Execution

The pipeline supports parallel execution at multiple levels:
- **Rule-level parallelism**: Multiple rules execute simultaneously
- **Thread-level parallelism**: Individual rules can use multiple threads
- **Algorithm-level parallelism**: Different algorithms train in parallel

## Results and Performance

### Model Performance Summary

Based on the latest pipeline execution:

| Algorithm | Test Accuracy | CV Accuracy (Mean ± Std) |
|-----------|---------------|---------------------------|
| SVM | 0.9667 | 0.9750 ± 0.0204 |
| Logistic Regression | 0.9667 | 0.9667 ± 0.0167 |
| Gradient Boosting | 0.9667 | 0.9667 ± 0.0167 |
| Random Forest | 0.9000 | 0.9500 ± 0.0167 |

### Best Performing Model
**SVM** achieved the highest performance with 96.67% test accuracy and excellent cross-validation stability.

## Monitoring and Notifications

### Health Checks
- Automatic validation of pipeline outputs
- Data integrity verification
- Model file existence checks
- Metric value validation

### Notifications
- Pipeline completion notifications
- Best model performance reporting
- Slack webhook integration support
- Comprehensive logging

## Screenshots

### Pipeline Execution
![Pipeline DAG](reports/rulegraph.png)
*Figure 1: Snakemake workflow DAG visualization*

### Performance Report
The pipeline generates comprehensive Markdown reports with:
- Executive summary with best performing models
- Detailed performance comparison tables
- Cross-validation results
- Configuration details
- Recommendations for production deployment

## Integration with Existing Tools

### MLflow Integration
- Automatic experiment tracking
- Model parameter logging
- Performance metric recording
- Model artifact storage

### DVC Integration
- Data versioning support
- Pipeline reproducibility
- Large file management

## Scalability and Reproducibility

### Reproducibility Features
- Fixed random seeds for consistent results
- Version-controlled configurations
- Deterministic data splits
- Comprehensive logging

### Scalability Features
- Parallel execution support
- Modular rule design
- Configurable resource allocation
- Extensible architecture

## Configuration Examples

### Base Configuration
```yaml
seed: 42
experiment_name: "ml_pipeline_experiment"
data:
  name: iris
  test_size: 0.2
model:
  algorithm: random_forest
evaluation:
  cross_validation: true
  cv_folds: 5
```

### Algorithm-Specific Configuration
```yaml
# SVM Configuration
algorithm: svm
hyperparameters:
  C: 1.0
  kernel: rbf
  gamma: scale
  random_state: 42
```

## Future Enhancements

### Potential Improvements
1. **Additional Algorithms**: Support for neural networks, ensemble methods
2. **Hyperparameter Tuning**: Integration with Optuna or Hyperopt
3. **Advanced Monitoring**: Real-time pipeline monitoring dashboards
4. **Model Serving**: Automatic model deployment capabilities
5. **Data Sources**: Support for additional datasets and data formats

### Production Deployment
1. **Containerization**: Docker integration for reproducible environments
2. **Orchestration**: Kubernetes integration for cluster deployment
3. **CI/CD Integration**: Automated testing and deployment pipelines
4. **Model Monitoring**: Production model performance monitoring

## Conclusion

This implementation successfully demonstrates the power of modern ML pipeline orchestration using Snakemake and Hydra. The pipeline provides:

- **Reproducible Workflows**: Complete automation with dependency management
- **Flexible Configuration**: Hierarchical configuration system with validation
- **Scalable Execution**: Parallel processing and resource optimization
- **Comprehensive Monitoring**: Health checks, notifications, and reporting
- **Production Ready**: Integration with MLflow and DVC for enterprise deployment

The pipeline achieves excellent performance on the Iris classification task, demonstrating the effectiveness of the chosen orchestration tools for automated machine learning workflows.

---

*Report generated for HW4: Automated ML Pipelines*
*Tools: Snakemake + Hydra*
*Date: December 2025*
