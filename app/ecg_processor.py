import numpy as np
import h5py
import logging

# Initialize logger for the ECGProcessor
logger = logging.getLogger(__name__)


class ECGProcessor:
    def __init__(self, ecg_shape, ecg_leads, ecg_hd5_path):
        self.ecg_shape = ecg_shape
        self.ecg_leads = ecg_leads
        self.ecg_hd5_path = ecg_hd5_path
        logger.info(
            "ECGProcessor initialized with shape: %s, leads: %s", ecg_shape, ecg_leads
        )

    def ecg_as_tensor(self, ecg_file):
        logger.info("Processing ECG file: %s", ecg_file)
        try:
            with h5py.File(ecg_file, "r") as hd5:
                tensor = np.zeros(self.ecg_shape, dtype=np.float32)
                for lead in self.ecg_leads:
                    data = np.array(hd5[f"{self.ecg_hd5_path}/{lead}/instance_0"])
                    tensor[:, self.ecg_leads[lead]] = data
                    logger.debug("Loaded data for lead %s", lead)

                tensor -= np.mean(tensor)
                tensor /= np.std(tensor) + 1e-6
                logger.info("ECG file processed successfully: %s", ecg_file)

            return np.expand_dims(tensor, axis=0)
        except Exception as e:
            logger.error("Failed to process ECG file: %s", e)
            raise ValueError(f"Failed to process ECG file: {e}")
