"""
Module to store the constant variables
"""

from decouple import config

CERT_FOLDER = config("KAFKA_CERT_FOLDER")
SERVICE_URI = config("KAFKA_SERVICE_URI")
TOPIC_NAME = config("KAFKA_TOPIC_NAME")
MAX_READ_TRIES = 5
