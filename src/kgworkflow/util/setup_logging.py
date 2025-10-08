import logging
import logging.config
import os
import yaml

def setup_logging(
    default_path='logging.yaml',
    default_level=logging.INFO,
    env_key='LOGGING_CONFIG'
):
    """
    Set up the logging configuration for the application.

    This function initializes the logging system by loading configuration from a
    specified file (defaults to `logging.yaml`) or an environment variable (if
    specified). If the designated configuration file is not found, it falls back
    to a basic logging configuration with the set log level.

    :param default_path: The default path of the logging configuration file
        (default is 'logging.yaml').
    :type default_path: str
    :param default_level: The default logging level to use if no configuration
        file is found (default is `logging.INFO`).
    :type default_level: int
    :param env_key: The environment variable key to refer for the logging
        configuration file path.
    :type env_key: str
    :return: None
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