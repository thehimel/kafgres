"""Test the insert module."""

from sqlalchemy.engine.base import Engine
from src.core.insert import init_db, insert_data, get_data, vaccination_data
from src.core.utilities.constants import PG_SERVICE_URI
from src.core.utilities.data import person
from src.core.models import Vaccination


def test_init_db():
    """Test database initialization."""

    engine = init_db(PG_SERVICE_URI)
    assert isinstance(engine, Engine)


def test_vaccination_date():
    """Test the conversion from person data to vaccination data."""
    person_data = person()[0]
    v_data = vaccination_data(person_data)
    assert isinstance(v_data, Vaccination)


def test_send_data():
    """Test sending of data."""

    db_engine = init_db(PG_SERVICE_URI)
    person_data = person()[0]
    insert_data(engine=db_engine, data=person_data)
    fetched_data = get_data(engine=db_engine, data_id=person_data["id"])
    assert vaccination_data(person_data).id == fetched_data.id
