from tensorflow.keras.models import load_model
from ml4h.tensormap.ukb.survival import mgb_afib_wrt_instance2
from ml4h.tensormap.ukb.demographics import age_2_wide, af_dummy, sex_dummy3
from ml4h.models.model_factory import get_custom_objects
import logging

# Initialize logger for the ECGModel
logger = logging.getLogger(__name__)


class ECGModel:
    """
    A class to handle the loading and prediction of ECG data using a pre-trained model.

    Attributes:
        model (tensorflow.keras.Model): The loaded ECG model.
        output_tensormaps (dict): A dictionary mapping output tensor names to their corresponding tensormap objects.
        model_output_names (list): A list of the model's output layer names.
    """

    def __init__(self, model_path):
        """
        Initialize the ECGModel by loading the model from the given path and setting up output tensormaps.

        Args:
            model_path (str): The file path to the pre-trained ECG model.
        """
        logger.info("Initializing ECGModel with model path: %s", model_path)
        self.model = self.load_model_from_path(model_path)  # Load the model
        self.output_tensormaps = self._init_output_tensormaps()  # Initialize output tensormaps
        self.model_output_names = self.tf_model_output_names()  # Get model output names
        logger.info("ECGModel initialized successfully")

    def load_model_from_path(self, model_path):
        """
        Load the pre-trained ECG model from the specified file path.

        Args:
            model_path (str): The path to the model file.

        Returns:
            tensorflow.keras.Model: The loaded model.

        Raises:
            RuntimeError: If the model fails to load from the given path.
        """
        logger.info("Loading model from path: %s", model_path)
        custom_dict = get_custom_objects(
            [mgb_afib_wrt_instance2, age_2_wide, af_dummy, sex_dummy3]
        )  # Get custom objects required by the model
        try:
            self.tf_model = load_model(model_path, custom_objects=custom_dict)  # Load model with custom objects
            logger.info("Model loaded successfully from: %s", model_path)
        except Exception as e:
            logger.error("Failed to load model from path %s: %s", model_path, e)
            raise RuntimeError(f"Failed to load model: {e}")
        return self.tf_model

    def tf_model_output_names(self):
        """
        Retrieve the output names of the loaded TensorFlow model.

        Returns:
            list: A list of output layer names of the model.
        """
        output_names = self.tf_model.output_names
        logger.debug("Model output names: %s", output_names)
        return output_names

    def _init_output_tensormaps(self):
        """
        Initialize the output tensormaps used by the model.

        The tensormaps provide metadata about each of the model's outputs, such as their shape and interpretation.

        Returns:
            dict: A dictionary mapping output names to their corresponding tensormap objects.
        """
        output_tensormaps = {
            tm.output_name(): tm
            for tm in [mgb_afib_wrt_instance2, age_2_wide, af_dummy, sex_dummy3]
        }
        logger.debug("Initialized output tensormaps: %s", output_tensormaps.keys())
        return output_tensormaps

    def predict(self, ecg_tensor):
        """
        Make predictions on the provided ECG tensor using the loaded model.

        Args:
            ecg_tensor (np.ndarray): A tensor containing preprocessed ECG data.

        Returns:
            list: A list of predictions corresponding to the model's outputs.
        """
        logger.info("Making predictions with ECG tensor of shape: %s", ecg_tensor.shape)
        predictions = self.model.predict(ecg_tensor)  # Make predictions with the model
        logger.info("Predictions made successfully")
        return predictions
