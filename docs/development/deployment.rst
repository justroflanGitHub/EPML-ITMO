Deployment Guide
================

This guide covers various deployment strategies for the Iris Data Science Project, from local development to production environments.

Local Development Deployment
-----------------------------

Running Locally
~~~~~~~~~~~~~~~

For local development and testing:

.. code-block:: bash

   # Install dependencies
   poetry install

   # Run the complete pipeline
   make all

   # Or run individual components
   make data
   make train
   make evaluate
   make report

Using Docker
~~~~~~~~~~~~

Containerized deployment for consistent environments:

.. code-block:: bash

   # Build the Docker image
   docker build -t iris-ml .

   # Run the complete pipeline
   docker run --rm -v $(pwd):/app iris-ml make all

   # Run interactive session
   docker run -it --rm -v $(pwd):/app iris-ml bash

   # Run specific commands
   docker run --rm -v $(pwd):/app iris-ml python src/run.py experiment.name="docker_test"

Docker Compose Setup
~~~~~~~~~~~~~~~~~~~~

For multi-service deployment:

.. code-block:: yaml

   # docker-compose.yml
   version: '3.8'
   services:
     iris-ml:
       build: .
       volumes:
         - .:/app
         - ./models:/app/models
         - ./reports:/app/reports
       environment:
         - MLFLOW_TRACKING_URI=http://mlflow:5000
         - CLEARML_API_ACCESS_KEY=${CLEARML_API_ACCESS_KEY}
         - CLEARML_API_SECRET_KEY=${CLEARML_API_SECRET_KEY}

     mlflow:
       image: ghcr.io/mlflow/mlflow:v2.17.0
       ports:
         - "5000:5000"
       environment:
         - BACKEND_STORE_URI=sqlite:///mlflow.db
       volumes:
         - ./mlruns:/mlflow/mlruns
         - ./mlflow.db:/mlflow.db

     clearml-server:
       image: allegroai/clearml:latest
       ports:
         - "8080:8080"
         - "8008:8008"
       environment:
         - CLEARML_HOST_IP=localhost
       volumes:
         - ./clearml_data:/opt/clearml/data

Production Deployment
----------------------

Model Serving with MLflow
~~~~~~~~~~~~~~~~~~~~~~~~~

Deploy models using MLflow Model Serving:

.. code-block:: bash

   # Serve a model locally
   mlflow models serve -m models:/iris_model/1 -p 5001

   # Build a Docker image for the model
   mlflow models build-docker -m models:/iris_model/1 -n iris-model

   # Run the model server
   docker run -p 5001:8080 iris-model

Model Serving with ClearML
~~~~~~~~~~~~~~~~~~~~~~~~~

Deploy models using ClearML Serving:

.. code-block:: python

   from clearml import Model
   from clearml.serving import ModelServer

   # Load registered model
   model = Model.get_model(model_id='your_model_id')

   # Deploy model
   server = ModelServer()
   endpoint = server.deploy_model(
       model=model,
       serving_platform='kubernetes',
       namespace='ml-serving'
   )

   print(f"Model deployed at: {endpoint}")

FastAPI Web Service
~~~~~~~~~~~~~~~~~~~

Create a REST API for model inference:

.. code-block:: python

   # app.py
   from fastapi import FastAPI, HTTPException
   from pydantic import BaseModel
   import joblib
   import numpy as np

   app = FastAPI(title="Iris Classification API")

   # Load model
   model = joblib.load('models/iris_model.pkl')

   class IrisFeatures(BaseModel):
       sepal_length: float
       sepal_width: float
       petal_length: float
       petal_width: float

   class_names = ['setosa', 'versicolor', 'virginica']

   @app.post("/predict")
   def predict(features: IrisFeatures):
       try:
           # Prepare input
           X = np.array([[features.sepal_length, features.sepal_width,
                         features.petal_length, features.petal_width]])

           # Make prediction
           prediction = model.predict(X)
           probabilities = model.predict_proba(X)

           return {
               "prediction": class_names[prediction[0]],
               "probabilities": {
                   class_names[i]: float(prob)
                   for i, prob in enumerate(probabilities[0])
               }
           }
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="0.0.0.0", port=8000)

Run the API server:

.. code-block:: bash

   # Install FastAPI
   pip install fastapi uvicorn

   # Run the server
   python app.py

   # Test the API
   curl -X POST "http://localhost:8000/predict" \
        -H "Content-Type: application/json" \
        -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'

Flask Web Application
~~~~~~~~~~~~~~~~~~~~~

Create a simple web interface:

.. code-block:: python

   from flask import Flask, request, jsonify, render_template
   import joblib
   import numpy as np

   app = Flask(__name__)

   # Load model
   model = joblib.load('models/iris_model.pkl')
   class_names = ['setosa', 'versicolor', 'virginica']

   @app.route('/')
   def home():
       return render_template('index.html')

   @app.route('/predict', methods=['POST'])
   def predict():
       try:
           # Get form data
           features = [
               float(request.form['sepal_length']),
               float(request.form['sepal_width']),
               float(request.form['petal_length']),
               float(request.form['petal_width'])
           ]

           # Make prediction
           X = np.array([features])
           prediction = model.predict(X)[0]
           probabilities = model.predict_proba(X)[0]

           return render_template('result.html',
                                prediction=class_names[prediction],
                                probabilities=probabilities,
                                class_names=class_names)
       except Exception as e:
           return str(e)

   if __name__ == "__main__":
       app.run(debug=True, host='0.0.0.0', port=5000)

Cloud Deployment
----------------

AWS Deployment
~~~~~~~~~~~~~~

Deploy to Amazon Web Services:

.. code-block:: bash

   # Build and push Docker image to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account.dkr.ecr.us-east-1.amazonaws.com
   docker build -t iris-ml .
   docker tag iris-ml:latest your-account.dkr.ecr.us-east-1.amazonaws.com/iris-ml:latest
   docker push your-account.dkr.ecr.us-east-1.amazonaws.com/iris-ml:latest

   # Deploy to ECS/Fargate
   aws ecs create-service --cluster your-cluster --service-name iris-service --task-definition iris-task --desired-count 1

Google Cloud Platform
~~~~~~~~~~~~~~~~~~~~~

Deploy to Google Cloud:

.. code-block:: bash

   # Build and push to GCR
   gcloud builds submit --tag gcr.io/your-project/iris-ml

   # Deploy to Cloud Run
   gcloud run deploy iris-service --image gcr.io/your-project/iris-ml --platform managed --port 8000

   # Or deploy to GKE
   kubectl apply -f k8s-deployment.yaml

Azure Deployment
~~~~~~~~~~~~~~~~

Deploy to Microsoft Azure:

.. code-block:: bash

   # Build and push to ACR
   az acr build --registry your-registry --image iris-ml:v1 .

   # Deploy to AKS
   az aks create --resource-group your-rg --name your-aks-cluster --node-count 1
   az aks get-credentials --resource-group your-rg --name your-aks-cluster
   kubectl apply -f k8s-deployment.yaml

Kubernetes Deployment
---------------------

Complete Kubernetes manifests:

.. code-block:: yaml

   # k8s-deployment.yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: iris-ml-deployment
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: iris-ml
     template:
       metadata:
         labels:
           app: iris-ml
       spec:
         containers:
         - name: iris-ml
           image: iris-ml:latest
           ports:
           - containerPort: 8000
           env:
           - name: MODEL_PATH
             value: "/models/iris_model.pkl"
           volumeMounts:
           - name: model-storage
             mountPath: /models
         volumes:
         - name: model-storage
           persistentVolumeClaim:
             claimName: model-pvc

   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: iris-ml-service
   spec:
     selector:
       app: iris-ml
     ports:
       - port: 80
         targetPort: 8000
     type: LoadBalancer

   ---
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: model-pvc
   spec:
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 10Gi

Helm Chart Deployment
~~~~~~~~~~~~~~~~~~~~~

Use Helm for package management:

.. code-block::

   charts/
   ├── iris-ml/
   │   ├── Chart.yaml
   │   ├── values.yaml
   │   ├── templates/
   │   │   ├── deployment.yaml
   │   │   ├── service.yaml
   │   │   ├── configmap.yaml
   │   │   └── ingress.yaml
   │   └── charts/

Deploy with Helm:

.. code-block:: bash

   # Install the chart
   helm install iris-ml ./charts/iris-ml

   # Upgrade deployment
   helm upgrade iris-ml ./charts/iris-ml

   # Uninstall
   helm uninstall iris-ml

CI/CD Integration
-----------------

GitHub Actions Deployment
~~~~~~~~~~~~~~~~~~~~~~~~~

Automated deployment pipeline:

.. code-block:: yaml

   # .github/workflows/deploy.yml
   name: Deploy to Production
   on:
     push:
       branches: [ main ]

   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v2
       - name: Run tests
         run: make test

     deploy:
       needs: test
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v2
       - name: Build and push Docker image
         run: |
           docker build -t iris-ml:${{ github.sha }} .
           docker tag iris-ml:${{ github.sha }} your-registry/iris-ml:latest
           docker push your-registry/iris-ml:latest

       - name: Deploy to Kubernetes
         run: |
           kubectl set image deployment/iris-ml iris-ml=your-registry/iris-ml:latest
           kubectl rollout status deployment/iris-ml

Jenkins Pipeline
~~~~~~~~~~~~~~~~

Jenkins deployment pipeline:

.. code-block:: groovy

   pipeline {
       agent any
       stages {
           stage('Test') {
               steps {
                   sh 'make test'
               }
           }
           stage('Build') {
               steps {
                   sh 'docker build -t iris-ml:${BUILD_NUMBER} .'
               }
           }
           stage('Deploy') {
               steps {
                   sh '''
                       kubectl set image deployment/iris-ml iris-ml=iris-ml:${BUILD_NUMBER}
                       kubectl rollout status deployment/iris-ml
                   '''
               }
           }
       }
       post {
           success {
               echo 'Deployment successful!'
           }
           failure {
               echo 'Deployment failed!'
           }
       }
   }

Monitoring and Observability
----------------------------

Model Performance Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Monitor model performance in production:

.. code-block:: python

   from src.models.model_monitor import ModelMonitor

   # Initialize monitor
   monitor = ModelMonitor(model_path='models/iris_model.pkl')

   # Set up monitoring
   monitor.enable_performance_tracking()
   monitor.enable_data_drift_detection(reference_data='data/train_features.pkl')

   # Check performance
   performance_report = monitor.generate_report()
   print(performance_report)

Infrastructure Monitoring
~~~~~~~~~~~~~~~~~~~~~~~~~

Monitor deployment infrastructure:

.. code-block:: bash

   # Check pod status
   kubectl get pods

   # View logs
   kubectl logs -f deployment/iris-ml

   # Check service endpoints
   kubectl get services

   # Monitor resource usage
   kubectl top pods

Health Checks
~~~~~~~~~~~~~

Implement health check endpoints:

.. code-block:: python

   @app.get("/health")
   def health_check():
       """Health check endpoint."""
       try:
           # Check model loading
           if model is None:
               raise Exception("Model not loaded")

           # Check basic prediction
           test_input = np.array([[5.1, 3.5, 1.4, 0.2]])
           prediction = model.predict(test_input)

           return {"status": "healthy", "model_loaded": True}
       except Exception as e:
           return {"status": "unhealthy", "error": str(e)}, 500

   @app.get("/metrics")
   def metrics():
       """Prometheus metrics endpoint."""
       return generate_latest(), 200, {'Content-Type': 'text/plain'}

Scaling Strategies
------------------

Horizontal Scaling
~~~~~~~~~~~~~~~~~~

Scale the deployment horizontally:

.. code-block:: bash

   # Scale Kubernetes deployment
   kubectl scale deployment iris-ml --replicas=5

   # Use HPA for automatic scaling
   kubectl autoscale deployment iris-ml --cpu-percent=70 --min=1 --max=10

Load Balancing
~~~~~~~~~~~~~~

Configure load balancing:

.. code-block:: yaml

   apiVersion: networking.k8s.io/v1
   kind: Ingress
   metadata:
     name: iris-ml-ingress
     annotations:
       nginx.ingress.kubernetes.io/rewrite-target: /
   spec:
     rules:
     - host: iris-ml.example.com
       http:
         paths:
         - path: /
           pathType: Prefix
           backend:
             service:
               name: iris-ml-service
               port:
                 number: 80

Model Versioning
----------------

Version Control for Models
~~~~~~~~~~~~~~~~~~~~~~~~~

Implement model versioning:

.. code-block:: python

   from src.models.model_registry import ModelRegistry

   # Initialize registry
   registry = ModelRegistry()

   # Register new model version
   version_info = registry.register_model(
       model_path='models/iris_model_v2.pkl',
       metadata={
           'accuracy': 0.98,
           'training_date': '2025-12-25',
           'algorithm': 'random_forest'
       }
   )

   # Promote to production
   registry.promote_to_production(version_info['version_id'])

   # Rollback if needed
   registry.rollback_to_version('v1.0')

A/B Testing
~~~~~~~~~~~

Implement A/B testing for model comparison:

.. code-block:: python

   from src.models.ab_testing import ABTester

   # Initialize A/B tester
   tester = ABTester()

   # Add models to test
   tester.add_variant('current', model_v1, weight=0.8)
   tester.add_variant('new', model_v2, weight=0.2)

   # Run test for a period
   results = tester.run_test(duration_days=7)

   # Analyze results
   if results['new']['accuracy'] > results['current']['accuracy']:
       print("New model performs better - promote to production")
   else:
       print("Keep current model")

Backup and Recovery
-------------------

Data Backup
~~~~~~~~~~~

Set up automated backups:

.. code-block:: bash

   # Backup models and data
   tar -czf backup_$(date +%Y%m%d).tar.gz models/ data/ config/

   # Upload to cloud storage
   aws s3 cp backup_$(date +%Y%m%d).tar.gz s3://your-backup-bucket/

   # Database backup (if using)
   pg_dump mlflow_db > mlflow_backup.sql

Disaster Recovery
~~~~~~~~~~~~~~~~~

Implement disaster recovery procedures:

.. code-block:: bash

   # Recovery script
   #!/bin/bash
   echo "Starting disaster recovery..."

   # Restore from backup
   aws s3 cp s3://your-backup-bucket/latest-backup.tar.gz .
   tar -xzf latest-backup.tar.gz

   # Redeploy application
   kubectl delete deployment iris-ml
   kubectl apply -f k8s-deployment.yaml

   # Verify recovery
   curl http://iris-ml.example.com/health

Security Considerations
-----------------------

API Security
~~~~~~~~~~~~

Secure the API endpoints:

.. code-block:: python

   from fastapi.security import HTTPBasic, HTTPBasicCredentials
   from fastapi import Depends, HTTPException, status

   security = HTTPBasic()

   def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
       """Basic authentication."""
       correct_username = "admin"
       correct_password = "secret"

       if not (credentials.username == correct_username and
               credentials.password == correct_password):
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Incorrect username or password",
               headers={"WWW-Authenticate": "Basic"},
           )
       return credentials.username

   @app.post("/predict")
   def predict(features: IrisFeatures, username: str = Depends(authenticate)):
       # Secure prediction endpoint
       # ... prediction logic ...

Model Security
~~~~~~~~~~~~~~

Protect model artifacts:

.. code-block:: bash

   # Encrypt model files
   openssl enc -aes-256-cbc -salt -in models/iris_model.pkl -out models/iris_model.enc -k your-encryption-key

   # Use secure model loading
   def load_secure_model(filepath, key):
       with open(filepath, 'rb') as f:
           encrypted_data = f.read()

       # Decrypt and load
       decrypted_data = decrypt_data(encrypted_data, key)
       return joblib.loads(decrypted_data)

Input Validation
~~~~~~~~~~~~~~~~

Validate API inputs:

.. code-block:: python

   from pydantic import BaseModel, validator

   class IrisFeatures(BaseModel):
       sepal_length: float
       sepal_width: float
       petal_length: float
       petal_width: float

       @validator('sepal_length', 'sepal_width', 'petal_length', 'petal_width')
       def validate_range(cls, v, field):
           """Validate feature ranges."""
           ranges = {
               'sepal_length': (4.0, 8.0),
               'sepal_width': (2.0, 5.0),
               'petal_length': (1.0, 7.0),
               'petal_width': (0.1, 3.0)
           }

           min_val, max_val = ranges[field.name]
           if not (min_val <= v <= max_val):
               raise ValueError(f'{field.name} must be between {min_val} and {max_val}')

           return v

Troubleshooting Deployment
---------------------------

Common Issues
~~~~~~~~~~~~~

**Container Issues:**

.. code-block:: bash

   # Check container logs
   docker logs container_id

   # Debug container
   docker run -it --entrypoint /bin/bash iris-ml

   # Check resource usage
   docker stats

**Kubernetes Issues:**

.. code-block:: bash

   # Check pod status
   kubectl describe pod pod_name

   # Check events
   kubectl get events --sort-by=.metadata.creationTimestamp

   # Debug pod
   kubectl exec -it pod_name -- /bin/bash

**API Issues:**

.. code-block:: bash

   # Test API endpoint
   curl -v http://localhost:8000/health

   # Check API logs
   docker logs api_container

   # Validate request format
   curl -X POST "http://localhost:8000/predict" \
        -H "Content-Type: application/json" \
        -d '{"invalid": "data"}'

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

Optimize deployment performance:

.. code-block:: bash

   # Profile application
   python -m cProfile -s time src/run.py > profile.txt

   # Optimize model loading
   # Use joblib with compression
   joblib.dump(model, 'model_compressed.pkl', compress=3)

   # Implement caching
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'redis'})

This comprehensive deployment guide covers everything from local development to production deployment with monitoring, scaling, and security considerations.
