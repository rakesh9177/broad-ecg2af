# ECG Prediction Gradio App

This project is an ECG prediction application built using Gradio, TensorFlow, and ML4H libraries. The app allows users to upload ECG files in HD5 format and receive multi-task predictions - atrial fibrillation survival curve predictions, sex and age classification, and atrial fibrillation detection. The project includes model processing, ECG data preprocessing, and visualization of the prediction results.

## Table of Contents

- [Installation](#installation)
- [Docker Setup](#docker-setup)
- [Google Cloud Deployment](#google-cloud-deployment)
- [Usage](#usage)
- [Key Components](#key-components)
  - [ECGModel](#ecgmodel)
  - [ECGProcessor](#ecgprocessor)
  - [Visualizer](#visualizer)
- [License](#license)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/rakesh9177/broad-ecg2af.git
    cd broad-ecg2af
    ```
## Docker Setup

Since you already have a `Dockerfile` in the repository, you can easily build and run the Docker container:

1. **Build the Docker image:**
    ```bash
    docker build -t broad-ecg2af .
    ```

2. **Run the Docker container:**
    ```bash
    docker run -p 7860:7860 broad-ecg2af
    ```

3. Access the app by navigating to `http://localhost:7860` in your web browser.

## Google Cloud Deployment

You can deploy this Docker container on Google Cloud using Google Cloud Run or Google Kubernetes Engine (GKE).

### Google Cloud Run

1. **Build the Docker image and push it to Google Container Registry (GCR):**
    ```bash
    gcloud builds submit --tag gcr.io/your-project-id/ecg-gradio-app .
    ```

2. **Deploy the container to Cloud Run:**
    ```bash
    gcloud run deploy ecg-gradio-app --image gcr.io/your-project-id/ecg-gradio-app --platform managed --port 7860
    ```

3. Once deployed, Google Cloud Run will provide you with a URL to access your Gradio app.

## Usage

1. The app will launch locally (or in Docker). You can access it by navigating to `http://localhost:7860` in your web browser.

2. Upload an ECG file in HD5 format, and the app will display the following predictions:
   - Survival curve prediction for incident atrial fibrillation.
   - Predicted sex (Male/Female).
   - Predicted age.
   - Atrial fibrillation classification.

## Key Components

### ECGModel

The `ECGModel` class handles loading the pre-trained TensorFlow model and making predictions on ECG data. It also manages custom objects required by the model and initializes output tensor maps that define how to interpret the model's outputs.

**Main Methods:**
- `load_model_from_path(model_path)`: Loads the TensorFlow model from the specified path.
- `tf_model_output_names()`: Retrieves the output names of the model.
- `predict(ecg_tensor)`: Takes the preprocessed ECG tensor and returns the model's predictions.

### ECGProcessor

The `ECGProcessor` class processes the raw ECG data from an HD5 file and converts it into a tensor format for prediction. It normalizes the ECG data by subtracting the mean and dividing by the standard deviation.

### Visualizer

The `Visualizer` class generates visualizations of the prediction results. The primary method is responsible for creating a horizontal bar chart that displays the predicted probabilities for different categories (e.g., male/female, yes/no).



The `ECGGradioApp` class is responsible for the overall functionality of the Gradio interface. It manages the flow of the app, from file upload to prediction and visualization.

**Main Methods:**
- `predict_ecg(file)`: Processes the uploaded ECG file and returns the prediction results.
- `_generate_outputs(predictions)`: Generates the necessary outputs (sliders and charts) based on the model's predictions.
- `launch()`: Launches the Gradio app.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
