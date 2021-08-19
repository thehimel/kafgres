"""
Module to store the constant variables
"""

import sys
from decouple import config, UndefinedValueError

MAX_WAIT = 10
MAX_READ_TRIES = 5

try:
    CERT_FOLDER = config("KAFKA_CERT_FOLDER")
    SERVICE_URI = config("KAFKA_SERVICE_URI")
    TOPIC_NAME = config("KAFKA_TOPIC_NAME")
    PG_SERVICE_URI = config("PG_SERVICE_URI")
    # replace 'postgres' with 'postgresql' for SQLAlchemy.
    if PG_SERVICE_URI.startswith("postgres://"):
        PG_SERVICE_URI = PG_SERVICE_URI.replace("postgres://", "postgresql://", 1)
    TABLE_NAME = config("PG_TABLE_NAME")

except UndefinedValueError as error:
    MSG = str(error)
    # Detect the end of first sentence.
    INDEX = MSG.find(". ")
    print(f"Environment variable {MSG[0: INDEX + 1]}")
    sys.exit(1)
