# ECG Prediction Gradio App

This project is an ECG prediction application built using Gradio, TensorFlow, and ML4H libraries. The app allows users to upload ECG files in HD5 format and receive multi-task predictions - atrial fibrillation survival curve predictions, sex and age classification, and atrial fibrillation detection. The project includes model processing, ECG data preprocessing, and visualization of the prediction results.

## Table of Contents

- [Installation](#installation)
- [Docker Setup](#docker-setup)
- [Google Cloud Deployment](#google-cloud-deployment)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Key Components](#key-components)
  - [ECGModel](#ecgmodel)
  - [ECGProcessor](#ecgprocessor)
  - [Visualizer](#visualizer)
  - [ECGGradioApp](#ecggradioapp)
- [License](#license)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/ecg-gradio-app.git
    cd ecg-gradio-app
    ```

2. Install the required dependencies locally if needed:
    ```bash
    pip install -r requirements.txt
    ```

3. Make sure you have a pre-trained model in HD5 format. Update the model path accordingly in the code.

## Docker Setup

Since you already have a `Dockerfile` in the repository, you can easily build and run the Docker container:

1. **Build the Docker image:**
    ```bash
    docker build -t ecg-gradio-app .
    ```

2. **Run the Docker container:**
    ```bash
    docker run -p 7860:7860 ecg-gradio-app
    ```

3. Access the app by navigating to `http://localhost:7860` in your web browser.

## Google Cloud Deployment

You can deploy this Docker container on Google Cloud using Google Cloud Run or Google Kubernetes Engine (GKE).

### Google Cloud Run

1. **Build the Docker image and push it to Google Container Registry (GCR):**
    ```bash
    gcloud builds submit --tag gcr.io/your-project-id/ecg-gradio-app
    ```

2. **Deploy the container to Cloud Run:**
    ```bash
    gcloud run deploy ecg-gradio-app --image gcr.io/your-project-id/ecg-gradio-app --platform managed --port 7860
    ```

3. Once deployed, Google Cloud Run will provide you with a URL to access your Gradio app.

### Google Kubernetes Engine (GKE)

1. **Push your Docker image to GCR:**
    ```bash
    docker tag ecg-gradio-app gcr.io/your-project-id/ecg-gradio-app
    docker push gcr.io/your-project-id/ecg-gradio-app
    ```

2. **Create a Kubernetes cluster:**
    ```bash
    gcloud container clusters create ecg-cluster --num-nodes=1
    ```

3. **Deploy the app to GKE:**

    Create a deployment file `deployment.yaml`:

    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: ecg-gradio-app
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: ecg-gradio-app
      template:
        metadata:
          labels:
            app: ecg-gradio-app
        spec:
          containers:
          - name: ecg-gradio-app
            image: gcr.io/your-project-id/ecg-gradio-app
            ports:
            - containerPort: 7860
    ```

    Apply the deployment:

    ```bash
    kubectl apply -f deployment.yaml
    ```

4. **Expose the app using a load balancer:**

    Create a service file `service.yaml`:

    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: ecg-gradio-app-service
    spec:
      type: LoadBalancer
      ports:
      - port: 80
        targetPort: 7860
      selector:
        app: ecg-gradio-app
    ```

    Apply the service:

    ```bash
    kubectl apply -f service.yaml
    ```

5. **Access the app**: GKE will assign an external IP address, and you can access your Gradio app via that IP.

## Usage

1. Start the Gradio app (if running locally or on Docker):
    ```bash
    python app/run_app.py
    ```

2. The app will launch locally (or in Docker). You can access it by navigating to `http://localhost:7860` in your web browser.

3. Upload an ECG file in HD5 format, and the app will display the following predictions:
   - Survival curve prediction for incident atrial fibrillation.
   - Predicted sex (Male/Female).
   - Predicted age.
   - Atrial fibrillation classification.

## Project Structure

