"""
Module to insert data to the PostgreSQL server.
"""

import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src.core.utilities.logger import logger
from src.core.models import Base, Vaccination


def vaccination_data(data):
    """
    Convert data to vaccination data.

    Arguments:
        data (dict): Data to convert.

    Returns:
        models.Vaccination
    """

    # Convert the id to uuid type.
    if isinstance(data["id"], str):
        data["id"] = uuid.UUID(data["id"])

    # Create an object.
    v_data = Vaccination(
        id=data["id"],
        name=data["name"],
        address=data["address"],
        phone_number=data["phone_number"],
        vaccinated=data["vaccinated"],
    )

    return v_data


def init_db(service_uri):
    """
    Initialize the Database.

    Arguments:
        service_uri (str): Service URI of the PostgreSQL server.

    Returns:
        sqlalchemy.engine.base.Engine
    """

    the_engine = create_engine(service_uri)

    # Create the table if doesn't exist.
    Base.metadata.create_all(the_engine)
    return the_engine


def insert_data(engine, data):
    """
    Insert the data.

    Arguments:
        engine (sqlalchemy.engine.base.Engine): SQLAlchemy Engine object.
        data (dict): Data to insert.

    Returns:
        bool
    """

    # Create a session.
    session_class = sessionmaker(bind=engine)
    session = session_class()

    success = True
    try:
        data = vaccination_data(data)
        session.add(data)
        session.commit()
        logger.info("Inserted: %s", data.repr_dict)

    except SQLAlchemyError as error:  # pylint: disable=broad-except
        logger.error("Commit to database server failed due to %s.", error)
        session.rollback()

        # for resetting non-committed .add()
        session.flush()
        success = False

    finally:
        session.close()

    return success


def get_data(engine, data_id):
    """
    Get the data.

    Arguments:
        engine (sqlalchemy.engine.base.Engine): SQLAlchemy Engine object.
        data_id (str): Id of the data.

    Returns:
        models.Vaccination
    """

    # Create a session.
    session_class = sessionmaker(bind=engine)
    session = session_class()

    try:
        fetched_data = session.query(Vaccination).get(data_id)
        logger.info("Fetched: %s", fetched_data.repr_dict)
        session.close()
        return fetched_data

    except SQLAlchemyError as error:  # pylint: disable=broad-except
        logger.error("Data retrieval from database failed due to %s.", error)
        session.close()
        return None
