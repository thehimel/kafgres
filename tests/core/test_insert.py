"""Test the insert module."""

from sqlalchemy.engine.base import Engine
from src.core.insert import init_db
from src.core.utilities.constants import PG_SERVICE_URI


def test_init_db():
    """Test database initialization."""

    engine = init_db(PG_SERVICE_URI)
    assert isinstance(engine, Engine)
