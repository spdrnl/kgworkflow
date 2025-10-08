import logging
import logging.config
import os
import yaml

def setup_logging(
    default_path='logging.yaml',
    default_level=logging.INFO,
    env_key='LOGGING_CONFIG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            configuration = yaml.safe_load(f.read())
        logging.config.dictConfig(configuration)
    else:
        logging.basicConfig(level=default_level)