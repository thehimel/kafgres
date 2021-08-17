"""
Module to insert data to the PostgreSQL server.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import uuid
from constants import PG_SERVICE_URI
from data import person
from models import Base, Vaccination
from logger import logger


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
        data (object): SQLAlchemy data object.

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
        logger.info(f"Inserted: %s", data.__repr__())

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
    data['id'] = uuid.UUID(data['id'])

    # Create an object.
    entry = Vaccination(id=data['id'],
                        name=data['name'],
                        address=data['address'],
                        phone_number=data['phone_number'],
                        vaccinated=data['vaccinated']
                        )

    insert_data(engine=engine, data=entry)


if __name__ == "__main__":
    """
    Send one data generated with Faker one each standalone run.
    """

    db_engine = init_db(PG_SERVICE_URI)
    person_data, key = person()
    send_data(engine=db_engine, data=person_data)
