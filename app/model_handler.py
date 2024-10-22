from tensorflow.keras.models import load_model
from ml4h.tensormap.ukb.survival import mgb_afib_wrt_instance2
from ml4h.tensormap.ukb.demographics import age_2_wide, af_dummy, sex_dummy3
from ml4h.models.model_factory import get_custom_objects
import logging

# Initialize logger for the ECGModel
logger = logging.getLogger(__name__)


class ECGModel:
    def __init__(self, model_path):
        logger.info("Initializing ECGModel with model path: %s", model_path)
        self.model = self.load_model_from_path(model_path)
        self.output_tensormaps = self._init_output_tensormaps()
        self.model_output_names = self.tf_model_output_names()
        logger.info("ECGModel initialized successfully")

    def load_model_from_path(self, model_path):
        logger.info("Loading model from path: %s", model_path)
        custom_dict = get_custom_objects(
            [mgb_afib_wrt_instance2, age_2_wide, af_dummy, sex_dummy3]
        )
        try:
            self.tf_model = load_model(model_path, custom_dict)
            logger.info("Model loaded successfully from: %s", model_path)
        except Exception as e:
            logger.error("Failed to load model from path %s: %s", model_path, e)
            raise RuntimeError(f"Failed to load model: {e}")
        return self.tf_model

    def tf_model_output_names(self):
        output_names = self.tf_model.output_names
        logger.debug("Model output names: %s", output_names)
        return output_names

    def _init_output_tensormaps(self):
        output_tensormaps = {
            tm.output_name(): tm
            for tm in [mgb_afib_wrt_instance2, age_2_wide, af_dummy, sex_dummy3]
        }
        logger.debug("Initialized output tensormaps: %s", output_tensormaps.keys())
        return output_tensormaps

    def predict(self, ecg_tensor):
        logger.info("Making predictions with ECG tensor of shape: %s", ecg_tensor.shape)
        predictions = self.model.predict(ecg_tensor)
        logger.info("Predictions made successfully")
        return predictions
