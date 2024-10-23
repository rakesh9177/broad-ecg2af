import numpy as np
import h5py
import logging

# Initialize logger for the ECGProcessor
logger = logging.getLogger(__name__)


class ECGProcessor:
    """
    A class used to process ECG files and convert them into a tensor format.

    Attributes:
        ecg_shape (tuple): The shape of the ECG tensor to be created.
        ecg_leads (dict): A dictionary mapping ECG leads to their corresponding indices.
        ecg_hd5_path (str): The path inside the HD5 file where ECG data is stored.
    """

    def __init__(self, ecg_shape, ecg_leads, ecg_hd5_path):
        """
        Initialize the ECGProcessor with the shape, leads, and HD5 file path.

        Args:
            ecg_shape (tuple): The shape of the ECG tensor to be created (e.g., (5000, 12)).
            ecg_leads (dict): A dictionary mapping ECG leads (e.g., {"lead_1": 0}) to indices in the tensor.
            ecg_hd5_path (str): The path inside the HD5 file where the ECG data is located.
        """
        self.ecg_shape = ecg_shape
        self.ecg_leads = ecg_leads
        self.ecg_hd5_path = ecg_hd5_path
        logger.info(
            "ECGProcessor initialized with shape: %s, leads: %s", ecg_shape, ecg_leads
        )

    def ecg_as_tensor(self, ecg_file):
        """
        Convert the ECG data from an HD5 file into a normalized tensor.

        Args:
            ecg_file (str): The path to the ECG file in HD5 format.

        Returns:
            np.ndarray: A numpy array containing the normalized ECG data, with an extra dimension for batch size.

        Raises:
            ValueError: If there is an error reading or processing the ECG file.
        """
        logger.info("Processing ECG file: %s", ecg_file)
        try:
            # Open the HD5 file and initialize an empty tensor with the specified shape
            with h5py.File(ecg_file, "r") as hd5:
                tensor = np.zeros(self.ecg_shape, dtype=np.float32)

                # Iterate over the ECG leads, loading the corresponding data into the tensor
                for lead in self.ecg_leads:
                    data = np.array(hd5[f"{self.ecg_hd5_path}/{lead}/instance_0"])
                    tensor[:, self.ecg_leads[lead]] = data
                    logger.debug("Loaded data for lead %s", lead)

                # Normalize the tensor by subtracting the mean and dividing by the standard deviation
                tensor -= np.mean(tensor)
                tensor /= np.std(tensor) + 1e-6
                logger.info("ECG file processed successfully: %s", ecg_file)

            # Add an extra dimension to the tensor for batch size (1 in this case)
            return np.expand_dims(tensor, axis=0)
        except Exception as e:
            logger.error("Failed to process ECG file: %s", e)
            raise ValueError(f"Failed to process ECG file: {e}")
