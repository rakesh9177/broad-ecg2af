import gradio as gr
import numpy as np
from app.model_handler import ECGModel
from app.ecg_processor import ECGProcessor
from app.visualizer import Visualizer
import logging
import os

# Initialize logger for the ECGGradioApp
logger = logging.getLogger(__name__)


class ECGGradioApp:
    """
    A class representing the Gradio app for ECG predictions.

    Attributes:
        model (ECGModel): The model used for making ECG predictions.
        processor (ECGProcessor): The processor used for preprocessing the ECG data.
        visualizer (Visualizer): The visualizer used for displaying prediction results.
    """

    def __init__(self, ecg_model, ecg_processor, visualizer):
        """
        Initialize the ECGGradioApp with model, processor, and visualizer.

        Args:
            ecg_model (ECGModel): The ECG model for making predictions.
            ecg_processor (ECGProcessor): The processor for converting ECG data into tensors.
            visualizer (Visualizer): The visualizer for generating charts from predictions.
        """
        logger.info("Initializing ECGGradioApp")
        self.model = ecg_model
        self.processor = ecg_processor
        self.visualizer = visualizer
        logger.info("ECGGradioApp initialized successfully")

    def predict_ecg(self, file):
        """
        Process the uploaded ECG file, make predictions, and return the results.

        Args:
            file (UploadedFile): The ECG file uploaded by the user.

        Returns:
            tuple: A tuple containing the predictions, including survival curve, sex classification, age prediction, and atrial fibrillation classification.

        Raises:
            gr.Error: If the file format is not HD5 or an error occurs during the prediction process.
        """
        logger.info("Received ECG file for prediction: %s", file)

        valid_extensions = ['.hd5']
        file_extension = os.path.splitext(file.name)[-1].lower()

        if file_extension not in valid_extensions:
            logger.error("Invalid file format: %s", file_extension)
            raise gr.Error("Invalid file format. Please upload a file in HD5 format.")

        try:
            ecg_tensor = self.processor.ecg_as_tensor(file)
            logger.debug("ECG tensor shape: %s", ecg_tensor.shape)
            predictions = self.model.predict(ecg_tensor)
            logger.info("Predictions made successfully")
            return self._generate_outputs(predictions)
        except Exception as e:
            logger.error("Error during prediction: %s", e)
            raise gr.Error("An error occurred while processing the ECG file. Check your file type and make sure it is in hd5 format")

    def _generate_outputs(self, predictions):
        """
        Generate outputs based on the model predictions.

        Args:
            predictions (list): The list of predictions made by the model.

        Returns:
            tuple: A tuple containing the generated outputs for survival curve, predicted sex, predicted age, and atrial fibrillation classification.
        """
        logger.info("Generating outputs from predictions")
        outputs = []
        for name, pred in zip(self.model.model_output_names, predictions):
            logger.debug("Processing output for: %s", name)
            otm = self.model.output_tensormaps[name]
            if otm.is_survival_curve():
                intervals = otm.shape[-1] // 2
                days_per_bin = 1 + otm.days_window // intervals
                predicted_survivals = np.cumprod(pred[:, :intervals], axis=1)
                outputs.append(1 - predicted_survivals[0, -1])
                logger.debug("Survival curve output generated for: %s", name)
            else:
                outputs.append(pred)

        output_1 = round(outputs[0], 3)
        output_2 = self.visualizer.plot_probability_bar_chart(
            [outputs[1][0][0], outputs[1][0][1]], labels=["Male", "Female"]
        )
        output_3 = round(outputs[2][0][0], 3)
        output_4 = self.visualizer.plot_probability_bar_chart(
            [outputs[3][0][0], outputs[3][0][1]], labels=["Yes", "No"]
        )

        logger.info("Outputs generated successfully")
        return output_1, output_2, output_3, output_4

    def launch(self):
        """
        Launch the Gradio app interface for ECG file upload and prediction.

        The interface allows users to upload an ECG file and receive predictions, which are displayed as sliders and plots.

        """
        logger.info("Launching Gradio interface")
        iface = gr.Interface(
            fn=self.predict_ecg,
            inputs=gr.File(label="Upload ECG File"),
            outputs=[
                gr.Slider(
                    label="Survival Curve Prediction for incident atrial fibrillation",
                    minimum=0,
                    maximum=1,
                    step=0.01,
                    info="This gives the probability score of survival curve for incident atrial fibrillation. Range(0 to 1)",
                ),
                gr.Plot(label="Individual Predicted Sex"),
                gr.Slider(
                    label="Predicted Age", minimum=0, maximum=100, step=0.1,
                    info="This gives the age prediction. Negative predicted values will be displayed as zero. Range(0 to 100)"
                ),
                gr.Plot(label="Classification of atrial fibrillation"),
            ],
            title="ECG2AF Model Predictions",
            description="Upload an ECG file in HD5 format to receive multi-task predictions.",
            theme=gr.themes.Base(),
        )

        iface.launch(server_name="0.0.0.0")
        logger.info("Gradio interface launched successfully")
