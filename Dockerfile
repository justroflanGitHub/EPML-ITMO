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

# Install project dependencies (including dev dependencies for container)
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Expose port if running Jupyter notebook (optional)
EXPOSE 8888

# Default command to run the pipeline
CMD ["python", "src/run.py", "pipeline"]
