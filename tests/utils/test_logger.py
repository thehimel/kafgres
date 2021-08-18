"""Test the logger."""
import logging
from src.utils.logger import logger


def test_logger():
    """Test the logger."""
    assert isinstance(logger, logging.Logger)
