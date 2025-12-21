# ML Pipeline Performance Report

Generated on: 2025-12-21 23:45:33

## Executive Summary

This report summarizes the performance of 4 different machine learning algorithms
trained on 1 datasets using automated Snakemake workflows with Hydra configuration management.

## Best Performing Models

### Highest Accuracy
- **Algorithm**: svm
- **Dataset**: iris
- **Accuracy**: 0.9667
- **F1-Score**: 0.9666

### Highest F1-Score
- **Algorithm**: svm
- **Dataset**: iris
- **Accuracy**: 0.9667
- **F1-Score**: 0.9666

## Detailed Results

### Performance Comparison
| Algorithm | Dataset | Accuracy | Precision (Macro) | Recall (Macro) | F1-Score (Macro) |
|-----------|---------|----------|-------------------|----------------|------------------|
| random_forest | iris | 0.9000 | 0.9024 | 0.9000 | 0.8997 |
| svm | iris | 0.9667 | 0.9697 | 0.9667 | 0.9666 |
| logistic_regression | iris | 0.9667 | 0.9697 | 0.9667 | 0.9666 |
| gradient_boosting | iris | 0.9667 | 0.9697 | 0.9667 | 0.9666 |

### Cross-Validation Results
| Algorithm | Dataset | CV Accuracy (Mean ± Std) | CV F1-Score (Mean ± Std) |
|-----------|---------|---------------------------|---------------------------|
| random_forest | iris | 0.9500 ± 0.0167 | N/A |
| svm | iris | 0.9750 ± 0.0204 | N/A |
| logistic_regression | iris | 0.9667 ± 0.0167 | N/A |
| gradient_boosting | iris | 0.9667 ± 0.0167 | N/A |

## Pipeline Configuration

### Tools Used
- **Workflow Orchestration**: Snakemake
- **Configuration Management**: Hydra
- **Experiment Tracking**: MLflow
- **Version Control**: DVC

### Algorithms Tested
- Random Forest
- Support Vector Machine (SVM)
- Logistic Regression
- Gradient Boosting

### Datasets
- Iris (classification, 3 classes, 150 samples)

## Recommendations

1. **Primary Model**: Use {best_accuracy['algorithm']} for production deployment
2. **Backup Model**: Consider {best_f1['algorithm']} for scenarios requiring balanced precision/recall
3. **Further Tuning**: All models show room for hyperparameter optimization
4. **Monitoring**: Implement continuous monitoring of model performance in production

---
*Report generated automatically by Snakemake pipeline*
