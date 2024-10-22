import yaml
from app.model_handler import ECGModel
from app.ecg_processor import ECGProcessor
from app.visualizer import Visualizer
from app.interface import ECGGradioApp
import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def get_model_path(model_path):
    """
    Resolve the correct path for the model. If the provided path is not absolute,
    convert it to an absolute path relative to the project root directory.
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if not os.path.isabs(model_path):
        model_path = os.path.join(project_root, model_path)

    return os.path.abspath(model_path)


with open("config/config.yaml") as f:
    config = yaml.safe_load(f)

# Initialize logging
logging.config.dictConfig(config["logging"])

# Log the model path
logger = logging.getLogger(__name__)

model_path = get_model_path(config["model_path"])
print(f"Model path**************** {model_path}")
model = ECGModel(model_path)
processor = ECGProcessor(
    ecg_shape=config["ecg_shape"],
    ecg_leads=config["ecg_leads"],
    ecg_hd5_path=config["ecg_hd5_path"],
)
visualizer = Visualizer()

app = ECGGradioApp(model, processor, visualizer)
app.launch()
