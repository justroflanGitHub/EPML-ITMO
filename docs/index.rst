Iris Data Science Project
=========================

.. image:: https://img.shields.io/badge/Python-3.13+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/badge/MLflow-2.17+-orange.svg
   :target: https://mlflow.org/
   :alt: MLflow Version

.. image:: https://img.shields.io/badge/scikit--learn-1.6+-green.svg
   :target: https://scikit-learn.org/
   :alt: Scikit-learn Version

**Comprehensive Data Science Workspace for Analyzing the Iris Dataset Using Modern Engineering Practices**

This project provides a complete MLOps pipeline for the classic Iris dataset classification problem, demonstrating best practices in data science project organization, experiment tracking, model versioning, and deployment.

Key Features
------------

* **Experiment Tracking**: Integrated MLflow and ClearML support
* **Data Versioning**: DVC for data and model versioning
* **Configuration Management**: Hydra for flexible configuration
* **Workflow Orchestration**: Snakemake for reproducible pipelines
* **Model Monitoring**: Health checks and performance monitoring
* **Automated Reporting**: Markdown reports with visualizations
* **Containerization**: Docker support for reproducible environments

Quick Start
-----------

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/justroflanGitHub/EPML-ITMO.git
   cd iris-data-science-project

   # Install dependencies
   poetry install

   # Run the complete pipeline
   make all

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart
   getting-started

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   usage
   configuration
   experiments
   commands

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/modules
   api/data
   api/models
   api/visualization

.. toctree::
   :maxdepth: 2
   :caption: Experiments & Reports

   reports/overview
   reports/mlflow
   reports/clearml
   reports/comparison

.. toctree::
   :maxdepth: 2
   :caption: Development

   development/contributing
   development/deployment
   development/reproducibility

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
