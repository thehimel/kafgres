"""
Module to store the constant variables
"""

from decouple import config


CERT_FOLDER = config("KAFKA_CERT_FOLDER")
SERVICE_URI = config("KAFKA_SERVICE_URI")
TOPIC_NAME = config("KAFKA_TOPIC_NAME")
MAX_WAIT = 10

PG_SERVICE_URI = config("PG_SERVICE_URI")
# replace 'postgres' with 'postgresql' for SQLAlchemy.
if PG_SERVICE_URI.startswith("postgres://"):
    PG_SERVICE_URI = PG_SERVICE_URI.replace("postgres://", "postgresql://", 1)

TABLE_NAME = config("PG_TABLE_NAME")
MAX_READ_TRIES = 5
