"""
Module to store the constant variables
"""

import sys
from decouple import config, UndefinedValueError
from logger import logger


def get_env(env):
    """
    Fetch an environment variable if exists.

    Arguments:
        env(str): Variable Name.

    Returns:
        str
    """

    try:
        return config(env)
    except UndefinedValueError as error:
        logger.exception(error)
        sys.exit(1)


CERT_FOLDER = get_env("KAFKA_CERT_FOLDER")
SERVICE_URI = get_env("KAFKA_SERVICE_URI")
TOPIC_NAME = get_env("KAFKA_TOPIC_NAME")
MAX_READ_TRIES = 5
