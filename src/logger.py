""""
Module to generate the logger.
"""

import logging
from constants import PROJECT_NAME


def get_logger():
    """"
    Get the logger.

    Returns:
        logger
    """

    # create logger
    logger = logging.getLogger(PROJECT_NAME)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to console_handler
    console_handler.setFormatter(formatter)

    # add console_handler to logger
    logger.addHandler(console_handler)

    return logger
