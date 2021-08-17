""""
Module to generate the logger.
"""

import logging


def get_logger():
    """"
    Get the logger.

    Returns:
        logger
    """

    # create logger
    project_name = "kafgres"
    logger = logging.getLogger(project_name)
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


logger = get_logger()
