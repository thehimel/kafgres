"""Test the constants"""

from os.path import exists

from src.core.utilities.constants import (
    CERT_FOLDER,
    SERVICE_URI,
    TOPIC_NAME,
    PG_SERVICE_URI,
    TABLE_NAME,
)


def test_constants():
    """Test the constants"""
    assert exists(CERT_FOLDER)
    assert isinstance(CERT_FOLDER, str)
    assert isinstance(SERVICE_URI, str)
    assert isinstance(TOPIC_NAME, str)
    assert isinstance(PG_SERVICE_URI, str)
    assert isinstance(TABLE_NAME, str)
