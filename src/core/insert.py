"""
Module to insert data to the PostgreSQL server.
"""

import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src.core.utilities.logger import logger
from src.core.models import Base, Vaccination


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
    Handle the data.

    Arguments:
        engine (sqlalchemy.engine.base.Engine): SQLAlchemy Engine object.
        data (models.Vaccination): SQLAlchemy data object.

    Returns:
        bool
    """

    # Create a session.
    session_class = sessionmaker(bind=engine)
    session = session_class()

    # Add and commit.
    session.add(data)

    success = True
    try:
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


def send_data(engine, data):
    """
    Send data to PostgreSQL server

    Arguments:
        engine (sqlalchemy.engine.base.Engine): SQLAlchemy Engine object.
        data (dict): Data to send.
    """
    # Convert the id to uuid type.
    data["id"] = uuid.UUID(data["id"])

    # Create an object.
    entry = Vaccination(
        id=data["id"],
        name=data["name"],
        address=data["address"],
        phone_number=data["phone_number"],
        vaccinated=data["vaccinated"],
    )

    insert_data(engine=engine, data=entry)
