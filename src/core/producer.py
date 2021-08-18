"""
Module for Producer.
"""

import sys
import random
import json
import time

from kafka import errors, KafkaProducer
from src.core.utilities.constants import CERT_FOLDER, SERVICE_URI, TOPIC_NAME
from src.core.utilities.data import person
from src.core.utilities.logger import logger


def get_producer(cert_folder, service_uri):
    """
    Get the producer.

    Arguments:
        cert_folder (str): Path to the directory where keys are stored.
        service_uri (str): 'host[:port]' string of the Kafka service.

    Returns:
        KafkaProducer
    """

    return KafkaProducer(
        bootstrap_servers=service_uri,
        security_protocol="SSL",
        ssl_cafile=cert_folder + "/ca.pem",
        ssl_keyfile=cert_folder + "/service.key",
        ssl_certfile=cert_folder + "/service.cert",
        value_serializer=lambda v: json.dumps(v).encode("ascii"),
        key_serializer=lambda k: json.dumps(k).encode("ascii"),
    )


def send_message(producer, topic_name, max_wait, index):
    """
    Send a message.

    Arguments:
        producer (KafkaProducer): The producer.
        topic_name (str): Name of the topic.
        max_wait (int): Maximum waiting time in seconds between the
            submission of two messages.
        index (int): Index number of the messages to be sent.

    Returns:
        tuple[KafkaProducer, int]
    """

    message, key = person()
    logger.info("Index: %d", index)
    logger.info("Sending: %s", message)

    # Sending the message to Kafka
    producer.send(topic_name, key=key, value=message)

    # Sleeping time
    sleep_time = random.randint(0, max_wait * 10) / 10
    logger.info("Sleeping: %ss", str(sleep_time))
    time.sleep(sleep_time)

    # Force flushing of all messages
    if (index % 100) == 0:
        producer.flush()
    index += 1

    return producer, index


def produce_messages(
    cert_folder=CERT_FOLDER,
    service_uri=SERVICE_URI,
    topic_name=TOPIC_NAME,
    nr_messages=-1,
    max_wait=10,
):
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
            value i.e. -1 to generate infinite number of messages. Default: -1.
        max_wait (int): Maximum waiting time in seconds between the
            submission of two messages. Default: 10.

    Returns:
        None
    """

    try:
        producer = get_producer(cert_folder=cert_folder, service_uri=service_uri)

    except errors.NoBrokersAvailable:
        logger.error("Producer setup failed as no broker is available.")
        sys.exit(1)

    except Exception as error:  # pylint: disable=broad-except
        logger.error("Producer setup failed due to %s.", error)
        sys.exit(1)

    if nr_messages <= 0:
        nr_messages = float("inf")

    index = 0
    while index < nr_messages:
        try:
            producer, index = send_message(producer, topic_name, max_wait, index)

        except Exception as error:  # pylint: disable=broad-except
            logger.error("Could not send message due to %s", error)

    producer.flush()
