Installation
============

This guide will help you set up the Iris Data Science Project on your local machine.

Prerequisites
-------------

Before installing the project, ensure you have the following prerequisites:

* **Python 3.13+**: Download from `python.org <https://www.python.org/downloads/>`_
* **Poetry**: For dependency management. Install with:

  .. code-block:: bash

     curl -sSL https://install.python-poetry.org | python3 -

* **Git**: For version control
* **Docker** (optional): For containerized deployment

System Requirements
-------------------

* **Operating System**: Linux, macOS, or Windows 10+
* **RAM**: Minimum 4GB, recommended 8GB+
* **Disk Space**: 2GB free space for the project and dependencies

Installation Steps
------------------

1. Clone the Repository
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/justroflanGitHub/EPML-ITMO.git
   cd iris-data-science-project

2. Install Dependencies
~~~~~~~~~~~~~~~~~~~~~~~

Using Poetry (recommended):

.. code-block:: bash

   # Install all dependencies
   poetry install

   # Activate the virtual environment
   poetry shell

Using pip (alternative):

.. code-block:: bash

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

3. Set Up Configuration
~~~~~~~~~~~~~~~~~~~~~~~

Copy the configuration files:

.. code-block:: bash

   # Copy configuration templates
   cp config/config.yaml config/config.local.yaml

   # Edit configuration as needed
   nano config/config.local.yaml

4. Initialize Data Versioning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Initialize DVC
   dvc init

   # Configure remote storage (optional)
   dvc remote add -d myremote /path/to/remote/storage

5. Set Up Experiment Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**MLflow Setup:**

.. code-block:: bash

   # Start MLflow tracking server
   mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000

**ClearML Setup:**

.. code-block:: bash

   # Configure ClearML
   clearml-init

   # Or set environment variables
   export CLEARML_WEB_HOST="https://app.clear.ml"
   export CLEARML_API_HOST="https://api.clear.ml"
   export CLEARML_FILES_HOST="https://files.clear.ml"
   export CLEARML_API_ACCESS_KEY="your_access_key"
   export CLEARML_API_SECRET_KEY="your_secret_key"

Verification
------------

After installation, verify everything is working:

.. code-block:: bash

   # Run health check
   python scripts/check_health.py

   # Run a simple test
   python -c "import src; print('Installation successful!')"

   # Check data pipeline
   make data

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Import Errors:**

If you encounter import errors, ensure all dependencies are installed:

.. code-block:: bash

   poetry install --no-cache
   # or
   pip install --upgrade -r requirements.txt

**Permission Errors:**

On Linux/macOS, you might need to adjust permissions:

.. code-block:: bash

   chmod +x scripts/*.py
   chmod +x scripts/*.sh

**DVC Issues:**

If DVC commands fail, reinitialize:

.. code-block:: bash

   rm -rf .dvc
   dvc init
   dvc repro

**MLflow/ClearML Connection Issues:**

Check your network configuration and API keys:

.. code-block:: bash

   # Test MLflow connection
   curl http://localhost:5000

   # Test ClearML connection
   clearml-task --help

Next Steps
----------

After successful installation:

1. Read the :doc:`quickstart` guide
2. Explore the :doc:`usage` examples
3. Learn about :doc:`configuration` options
4. Run your first :doc:`experiments`
