"""
singleton for endpoint configuration
"""

from .schema_loader import SchemaLoader, sl


class EndpointConfig:
    _instance = None
    _schema_loader: SchemaLoader = sl
    config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EndpointConfig, cls).__new__(cls)

            # # Put any initialization here.
            cls._instance.config = cls._schema_loader.load_endpoint_model()

        return cls._instance
