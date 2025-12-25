# Deployment Guide - Iris Data Science Project

## Overview

This guide provides comprehensive instructions for deploying the Iris Data Science Project in various environments, from local development to production deployment.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [GitHub Pages Setup](#github-pages-setup)
6. [Production Considerations](#production-considerations)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows 10/11
- **Python**: 3.13 or higher
- **Memory**: Minimum 4GB RAM, 8GB recommended
- **Storage**: 2GB free space for dependencies and data
- **Network**: Internet connection for package installation

### Required Software

- **Poetry**: Dependency management
- **Git**: Version control
- **Docker**: Containerization (optional)
- **Make**: Build automation (optional)

### Installing Prerequisites

#### Poetry Installation

```bash
# Using pip
pip install poetry

# Or using the official installer
curl -sSL https://install.python-poetry.org | python3 -

# Verify installation
poetry --version
```

#### Docker Installation

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
```

**macOS:**
```bash
brew install docker docker-compose
```

**Windows:**
Download and install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)

## Local Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/justroflanGitMO/EPML-ITMO.git
cd iris-data-science-project
```

### 2. Environment Setup

```bash
# Create virtual environment and install dependencies
poetry install

# Activate virtual environment
poetry shell

# Verify installation
python --version
poetry --version
```

### 3. Configuration

```bash
# Copy configuration template
cp config/config.yaml.example config/config.yaml

# Edit configuration as needed
vim config/config.yaml
```

### 4. Data Setup

```bash
# Download and prepare data
python scripts/download_data.py

# Verify data setup
python scripts/check_health.py
```

### 5. Run Development Pipeline

```bash
# Using Make
make all

# Or using Snakemake
snakemake --cores all

# Or run individual steps
snakemake data
snakemake train
snakemake evaluate
```

## Docker Deployment

### Building the Image

```bash
# Build Docker image
docker build -t iris-ds-project:latest .

# Verify image
docker images | grep iris-ds-project
```

### Running with Docker

```bash
# Run container
docker run -d --name iris-project iris-ds-project:latest

# Run with volume mounting
docker run -d -v $(pwd)/data:/app/data -v $(pwd)/models:/app/models iris-ds-project:latest

# Interactive mode
docker run -it --rm iris-ds-project:latest bash
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  iris-project:
    build: .
    volumes:
      - ./data:/app/data
      - ./models:/app/models
      - ./reports:/app/reports
    environment:
      - ENVIRONMENT=production
    ports:
      - "8000:8000"

  mlflow:
    image: python:3.13-slim
    command: mlflow ui --backend-store-uri sqlite:///mlruns/mlflow.db --host 0.0.0.0 --port 5000
    volumes:
      - ./models:/mlruns
    ports:
      - "5000:5000"
    working_dir: /mlruns
```

Run with:

```bash
docker-compose up -d
```

## Cloud Deployment

### AWS Deployment

#### Using AWS Batch

1. **Create Dockerfile for AWS:**
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY . .

RUN pip install poetry && \
    poetry config virtualenvs-create false && \
    poetry install --no-dev

CMD ["python", "src/run.py"]
```

2. **Deploy to AWS Batch:**
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

docker build -t iris-project .
docker tag iris-project:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/iris-project:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/iris-project:latest
```

#### Using SageMaker

```python
import sagemaker
from sagemaker.sklearn.estimator import SKLearn

# Create estimator
sklearn_estimator = SKLearn(
    entry_point='src/run.py',
    role='SageMakerRole',
    instance_type='ml.m5.large',
    framework_version='1.0-1',
    py_version='py3'
)

# Train model
sklearn_estimator.fit({'train': 's3://your-bucket/data/'})
```

### Google Cloud Platform

#### Using Cloud Run

```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT-ID/iris-project

# Deploy to Cloud Run
gcloud run deploy iris-project \
    --image gcr.io/PROJECT-ID/iris-project \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### Azure Deployment

#### Using Azure Container Instances

```bash
# Create resource group
az group create --name iris-project-rg --location eastus

# Create container instance
az container create \
    --resource-group iris-project-rg \
    --name iris-project \
    --image iris-project:latest \
    --cpu 2 \
    --memory 4 \
    --ports 8000
```

## GitHub Pages Setup

### 1. Enable GitHub Pages

1. Go to repository Settings
2. Navigate to Pages section
3. Select source: "GitHub Actions"

### 2. Deploy Documentation

The project includes automatic documentation deployment via GitHub Actions.

Trigger deployment:

```bash
# Push to main or hw_6 branch
git push origin main

# Or trigger manually via GitHub Actions UI
```

### 3. Custom Domain (Optional)

1. Add `CNAME` file to `docs/` directory
2. Configure DNS settings
3. Enable HTTPS in repository settings

## Production Considerations

### Security

#### Environment Variables

```bash
# Set production environment
export ENVIRONMENT=production
export MLFLOW_TRACKING_URI=postgresql://user:pass@host:5432/mlflow
export CLEARML_HOST=https://app.clear.ml
```

#### Secret Management

**AWS Secrets Manager:**
```bash
aws secretsmanager create-secret \
    --name iris-project/db-credentials \
    --secret-string '{"username":"user","password":"pass"}'
```

**Azure Key Vault:**
```bash
az keyvault secret set \
    --vault-name iris-project-vault \
    --name db-credentials \
    --value "user=username;password=password"
```

### Monitoring

#### Health Checks

```python
# Add to your application
@app.route('/health')
def health_check():
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }
```

#### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Scaling

#### Horizontal Scaling

- Use load balancers for API endpoints
- Implement stateless application design
- Use container orchestration (Kubernetes, ECS)

#### Vertical Scaling

- Monitor resource usage
- Adjust CPU/memory allocation
- Use auto-scaling groups

### Backup and Recovery

#### Database Backup

```bash
# MLflow tracking database backup
pg_dump mlflow_db > mlflow_backup_$(date +%Y%m%d).sql

# Model artifacts backup
tar -czf models_backup_$(date +%Y%m%d).tar.gz models/
```

#### Disaster Recovery

1. **Multi-region deployment**
2. **Automated backups**
3. **Recovery testing**
4. **Documentation procedures**

## CI/CD Pipeline

### GitHub Actions Workflow

The project includes a comprehensive CI/CD pipeline:

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          pip install poetry
          poetry install
      - name: Run tests
        run: poetry run pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to production
        run: |
          # Deployment commands
```

## Troubleshooting

### Common Issues

#### Poetry Installation Issues

```bash
# Clear Poetry cache
poetry cache clear --all pypi .

# Reinstall dependencies
poetry install --no-cache
```

#### Docker Build Issues

```bash
# Build with no cache
docker build --no-cache -t iris-project .

# Check Docker logs
docker logs iris-project
```

#### GitHub Pages Not Updating

1. Check Actions tab for failed workflows
2. Verify branch permissions
3. Ensure proper file structure

### Performance Issues

#### Slow Training

```python
# Use smaller datasets for testing
data = load_iris().data[:100]  # Use only first 100 samples

# Enable parallel processing
n_jobs = -1  # Use all available cores
```

#### Memory Issues

```python
# Process data in batches
for batch in pd.read_csv('data.csv', chunksize=1000):
    process_batch(batch)
```

### Getting Help

#### Logs and Diagnostics

```bash
# Collect system information
python -c "import sys; print(sys.version)"
python -c "import sklearn; print(sklearn.__version__)"

# Check MLflow installation
mlflow --version
```

#### Support Channels

- **GitHub Issues**: [Repository Issues](https://github.com/justroflanGitHub/EPML-ITMO/issues)
- **Documentation**: [Project Documentation](https://justroflanGitHub.github.io/EPML-ITMO/)
- **Email**: justroflanpochta@mail.ru

---

**Last Updated**: December 25, 2025
**Version**: 1.0.0
**Maintained by**: Mikhail
