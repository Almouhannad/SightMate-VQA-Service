import os
import yaml
from typing import Dict
from pydantic import BaseModel

class SMSASettings(BaseModel):
    model_path: str
    selector_path: str
    TAU: float
    threshold: float

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "SMSASettings":
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
            return cls(**config)

current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, "config.yaml")

smsa_settings = SMSASettings.from_yaml(config_path) 