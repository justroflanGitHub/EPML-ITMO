API Reference
=============

This section contains the complete API reference for the Iris Data Science Project.

.. note::
   This documentation is automatically generated. For the most up-to-date information, 
   please refer to the source code directly.

Project Structure
-----------------

The project is organized into several main modules:

* **src/data** - Data processing and preprocessing modules
* **src/models** - Machine learning models and training scripts  
* **src/visualization** - Visualization and plotting utilities
* **config** - Configuration files for different components

Data Processing
---------------

Data processing modules handle loading, cleaning, and preprocessing of the Iris dataset.

* **make_dataset.py** - Main data loading and preprocessing functionality
* **Data utilities** - Helper functions for data manipulation

Model Training and Evaluation
------------------------------

Machine learning models and training pipelines:

* **train_model.py** - Model training utilities
* **predict_model.py** - Prediction and inference functions
* **compare_experiments.py** - Experiment comparison and analysis

Experiment Tracking
-------------------

MLOps and experiment tracking modules:

* **mlflow_utils.py** - MLflow integration utilities
* **clearml_pipeline.py** - ClearML pipeline management
* **pipeline_monitor.py** - Pipeline monitoring and health checks

Visualization
-------------

Data visualization and plotting utilities:

* **visualize.py** - Plotting and visualization functions
* **Charts and graphs** - Performance visualization tools

Main Entry Point
----------------

* **src/run.py** - Main application entry point

Configuration
-------------

Configuration files are organized in the ``config/`` directory:

* **config.yaml** - Main configuration file
* **config/hydra/** - Hydra configuration files
* **config/clearml/** - ClearML-specific configurations

Usage Examples
--------------

For detailed usage examples and tutorials, please refer to:

* :doc:`../usage` - General usage guide
* :doc:`../quickstart` - Quick start tutorial
* :doc:`../experiments` - Running experiments guide

.. note::
   For detailed API documentation of specific functions and classes,
   please refer to the inline documentation in the source code.
