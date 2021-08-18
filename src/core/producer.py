"""
Module for Producer.
"""

import sys
import random
import json
import time

from kafka import errors, KafkaProducer
from src.core.utilities.constants import CERT_FOLDER, SERVICE_URI, TOPIC_NAME, MAX_WAIT
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

    try:
        return KafkaProducer(
            bootstrap_servers=service_uri,
            security_protocol="SSL",
            ssl_cafile=cert_folder + "/ca.pem",
            ssl_keyfile=cert_folder + "/service.key",
            ssl_certfile=cert_folder + "/service.cert",
            value_serializer=lambda v: json.dumps(v).encode("ascii"),
            key_serializer=lambda k: json.dumps(k).encode("ascii"),
        )

    except errors.NoBrokersAvailable:
        logger.error("Producer setup failed as no broker is available.")
        return None

    except Exception as error:  # pylint: disable=broad-except
        logger.error("Producer setup failed due to %s.", error)
        return None


def send_message(producer, topic_name, data, max_wait, index=0):
    """
    Send a message.

    Arguments:
        producer (KafkaProducer): The producer.
        topic_name (str): Name of the topic.
        data (tuple): Message and key packed in a tuple.
        max_wait (int): Maximum waiting time in seconds between the
            submission of two messages.
        index (int, optional): Index number of the messages to be sent.
            Default: 0.

    Returns:
        tuple[KafkaProducer, int]
    """

    message, key = data
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
    max_wait=MAX_WAIT,
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

    producer = get_producer(cert_folder=cert_folder, service_uri=service_uri)

    if producer is None:
        sys.exit(1)

    if nr_messages <= 0:
        nr_messages = float("inf")

    index = 0
    while index < nr_messages:
        try:
            producer, index = send_message(
                producer=producer,
                topic_name=topic_name,
                data=person(),
                max_wait=max_wait,
                index=index,
            )

        except Exception as error:  # pylint: disable=broad-except
            logger.error("Could not send message due to %s", error)

    producer.flush()
