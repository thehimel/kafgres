"""Module to test data package"""

import uuid
from src.core.utilities.data import unique_id, person


def test_unique_id():
    """Test if the function returns a valid uuid."""
    assert isinstance(unique_id(), uuid.UUID)


def test_person():
    """Test the data returned by person()"""
    message, key = person()
    items = ["id", "name", "address", "phone_number", "vaccinated"]

    # Test if the items are present in the message
    for item in items:
        assert item in message

    # Test if both ids are same.
    assert key["id"] == message["id"]

    # Test if the id can be converted to uuid object
    #   that is required to send data.
    assert uuid.UUID(key["id"])
