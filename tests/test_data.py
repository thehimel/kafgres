import uuid
from src.data import unique_id


def test_unique_id():
    """Test if the function returns a valid uuid."""
    assert isinstance(unique_id(), uuid.UUID)
