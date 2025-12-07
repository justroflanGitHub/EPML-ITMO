# Use the official Python base image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the project files
COPY . /app

# Install Poetry for dependency management
RUN pip install poetry

# Regenerate poetry.lock file to ensure it's in sync with pyproject.toml
RUN poetry lock

# Install project dependencies (including dev dependencies for container)
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Install DVC separately (compatibility issues with Poetry and Python 3.13)
RUN pip install dvc

# Expose port if running Jupyter notebook (optional)
EXPOSE 8888

# Default command to run the pipeline
CMD ["python", "src/run.py", "pipeline"]
