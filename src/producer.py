"""
Module for Producer.
"""

import logging
import sys
import random
import json
import time
from decouple import config
from kafka import errors, KafkaProducer
from data import person


CERT_FOLDER = config("KAFKA_CERT_FOLDER")
SERVICE_URI = config("KAFKA_SERVICE_URI")
TOPIC_NAME = config("KAFKA_TOPIC_NAME")

# Configure logging to print in stdout.
logging.basicConfig(level=logging.INFO)


def produce_messages(cert_folder=CERT_FOLDER,
                     service_uri=SERVICE_URI,
                     topic_name=TOPIC_NAME,
                     nr_messages=2,
                     max_wait=2):
    """
    Produce messages to Kafka.

    Arguments:
        cert_folder (str): Path to the directory where keys are stored.
            Default: Fetched from environment variable 'KAFKA_CERT_FOLDER'.
        service_uri (str): 'host[:port]' string of the Kafka service.
            Default: Fetched from environment variable 'KAFKA_SERVICE_URI'.
        topic_name (str): Name of the topic.
            Default: Fetched from environment variable 'KAFKA_TOPIC_NAME'.
        nr_messages(int): Number of total messages to be sent. Set a negative
            value i.e. -1 to generate infinite number of messages. Default: 2.
        max_wait (int): Maximum waiting time in seconds between the
            submission of two messages. Default: 2.

    Returns:
        None
    """

    try:
        producer = KafkaProducer(
            bootstrap_servers=service_uri,
            security_protocol="SSL",
            ssl_cafile=cert_folder+"/ca.pem",
            ssl_certfile=cert_folder+"/service.cert",
            ssl_keyfile=cert_folder+"/service.key",
            value_serializer=lambda v: json.dumps(v).encode('ascii'),
            key_serializer=lambda v: json.dumps(v).encode('ascii')
        )

    except errors.NoBrokersAvailable:
        logging.error("Producer setup failed as no broker is available.")
        sys.exit(1)

    except Exception as exp:  # pylint: disable=broad-except
        logging.error("Producer setup failed due to %s.", exp)
        sys.exit(1)

    if nr_messages <= 0:
        nr_messages = float('inf')

    i = 0
    while i <= nr_messages:
        message, key = person()
        logging.info("Sending: %s", message)

        try:
            # Sending the message to Kafka
            producer.send(topic_name, key=key, value=message)

            # Sleeping time
            sleep_time = random.randint(0, max_wait * 10)/10
            logging.info("Sleeping for %ss", str(sleep_time))
            time.sleep(sleep_time)

            # Force flushing of all messages
            if (i % 100) == 0:
                producer.flush()
            i = i + 1

        except Exception as exp:  # pylint: disable=broad-except
            logging.error("Could not send message due to %s", exp)

    producer.flush()


if __name__ == "__main__":
    produce_messages()
