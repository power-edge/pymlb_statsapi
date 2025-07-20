"""
created by nikos at 5/12/21
"""
import yaml

from . import CONFIGS_PATH
from .schema_loader import sl


class EndpointConfig:
    _instance = None
    config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EndpointConfig, cls).__new__(cls)

            # # Put any initialization here.
            # with open(f"{CONFIGS_PATH}/endpoint-model.yaml", 'r') as f:
            #     cls._instance.config = yaml.safe_load(f)
            cls._instance.config = sl.load_endpoint_model()

        return cls._instance
