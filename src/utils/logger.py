""""
Module to generate the logger.
"""

import logging


def get_logger():
    """ "
    Get the logger.

    Returns:
        logger
    """

    # Create logger
    project_name = "kafgres"
    the_logger = logging.getLogger(project_name)
    the_logger.setLevel(logging.DEBUG)

    # Create console handler and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Add formatter to console_handler
    console_handler.setFormatter(formatter)

    # Add console_handler to logger
    the_logger.addHandler(console_handler)

    return the_logger


logger = get_logger()
