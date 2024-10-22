import pytest
import numpy as np
import yaml
from app.ecg_processor import ECGProcessor  # Adjust import based on your structure

@pytest.fixture
def processor():
    # Load the configuration from the YAML file
    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)

    ecg_shape = config["ecg_shape"]  # Example shape
    ecg_leads = config["ecg_leads"]  # Load leads from config
    ecg_hd5_path = config["ecg_hd5_path"]  # Load HD5 path from config
    return ECGProcessor(ecg_shape, ecg_leads, ecg_hd5_path)

def test_ecg_as_tensor(processor):
    ecg_file = 'data/fake_0.hd5'
    tensor = processor.ecg_as_tensor(ecg_file)
    assert tensor.shape == (1, *processor.ecg_shape)  # Check the shape

def test_ecg_as_tensor_invalid_file(processor):
    with pytest.raises(ValueError):
        processor.ecg_as_tensor('invalid_file.hd5')
