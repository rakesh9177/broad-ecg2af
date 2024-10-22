import gradio as gr
import numpy as np
from app.model_handler import ECGModel
from app.ecg_processor import ECGProcessor
from app.visualizer import Visualizer
import logging

# Initialize logger for the ECGGradioApp
logger = logging.getLogger(__name__)


class ECGGradioApp:
    def __init__(self, ecg_model, ecg_processor, visualizer):
        logger.info("Initializing ECGGradioApp")
        self.model = ecg_model
        self.processor = ecg_processor
        self.visualizer = visualizer
        logger.info("ECGGradioApp initialized successfully")

    def predict_ecg(self, file):
        logger.info("Received ECG file for prediction: %s", file)
        try:
            ecg_tensor = self.processor.ecg_as_tensor(file)
            logger.debug("ECG tensor shape: %s", ecg_tensor.shape)
            predictions = self.model.predict(ecg_tensor)
            logger.info("Predictions made successfully")
            return self._generate_outputs(predictions)
        except Exception as e:
            logger.error("Error during prediction: %s", e)
            return None  # Handle this according to your app's needs

    def _generate_outputs(self, predictions):
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

        output_1 = outputs[0]
        output_2 = self.visualizer.plot_probability_bar_chart(
            [outputs[1][0][0], outputs[1][0][1]], labels=["Male", "Female"]
        )
        output_3 = outputs[2][0][0]
        output_4 = self.visualizer.plot_probability_bar_chart(
            [outputs[3][0][0], outputs[3][0][1]]
        )

        logger.info("Outputs generated successfully")
        return output_1, output_2, output_3, output_4

    def launch(self):
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
                    elem_id="gradient-slider",
                    elem_classes=["slider-label"],
                ),
                gr.Plot(label="Predicted Sex"),
                gr.Slider(label="Predicted Age", minimum=0, maximum=100, step=0.1),
                gr.Plot(label="Classification of atrial fibrillation"),
            ],
            title="ECG2AF Model Predictions",
            description="Upload an ECG file in HD5 format to receive multi-task predictions.",
            theme=gr.themes.Base(),
        )

        iface.launch()
        logger.info("Gradio interface launched successfully")
