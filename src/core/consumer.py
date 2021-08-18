"""
Module for Consumer.
"""

import sys
import json
from kafka import errors, KafkaConsumer
from src.core.utilities.constants import (
    CERT_FOLDER,
    SERVICE_URI,
    TOPIC_NAME,
    MAX_READ_TRIES,
)
from src.core.utilities.logger import logger
from src.core.insert import insert_data


def get_consumer(
        cert_folder,
        service_uri,
        topic_name,
        consumer_timeout_ms=float('inf')
):
    """
    Get the consumer.

    Arguments:
        cert_folder (str): Path to the directory where keys are stored.
        service_uri (str): 'host[:port]' string of the Kafka service.
        topic_name (str): Path to the directory where keys are stored.
        consumer_timeout_ms (float): Stop consumer if no messages is
            received within the defined time in milliseconds.
            Default: forever [float(‘inf’)].

    Returns:
        KafkaConsumer
    """

    try:
        # auto_offset_reset="earliest" to read the old messages.
        # Important Note: client_id and group_id are arbitrary and
        #   required to avoid reading the messages again.
        return KafkaConsumer(
            topic_name,
            auto_offset_reset="earliest",
            client_id="kafka-client-1",
            group_id="kafka-group-1",
            bootstrap_servers=service_uri,
            security_protocol="SSL",
            ssl_cafile=cert_folder + "/ca.pem",
            ssl_certfile=cert_folder + "/service.cert",
            ssl_keyfile=cert_folder + "/service.key",
            value_deserializer=lambda v: json.loads(v.decode("ascii")),
            key_deserializer=lambda v: json.loads(v.decode("ascii")),
            consumer_timeout_ms=consumer_timeout_ms
        )

    except errors.NoBrokersAvailable:
        logger.error("Producer setup failed as no broker is available.")
        return None

    except Exception as error:  # pylint: disable=broad-except
        logger.error("Consumer setup failed due to %s.", error)
        return None


def read_message(message):
    """
    Read the message.

    Arguments:
        message (kafka.consumer.fetcher.ConsumerRecord): Message to read.

    Returns:
        dict
    """

    logger.info(
        "Received: %s:%d:%d: key=%s value=%s",
        message.topic,
        message.partition,
        message.offset,
        message.key,
        message.value,
    )

    return message.value


def consume_message(
    engine, cert_folder=CERT_FOLDER, service_uri=SERVICE_URI, topic_name=TOPIC_NAME
):
    """
    Consumer messages from Kafka.

    Arguments:
        engine (sqlalchemy.engine.base.Engine): SQLAlchemy Engine object.
        cert_folder (str): Path to the directory where keys are stored.
            Default: Fetched from environment variable 'KAFKA_CERT_FOLDER'.
        service_uri (str): 'host[:port]' string of the Kafka service.
            Default: Fetched from environment variable 'KAFKA_SERVICE_URI'.
        topic_name (str): Name of the topic.
            Default: Fetched from environment variable 'KAFKA_TOPIC_NAME'.

    Returns:
        None
    """

    consumer = get_consumer(
        cert_folder=cert_folder, service_uri=service_uri, topic_name=topic_name
    )

    if consumer is None:
        sys.exit(1)

    tries = 0

    for message in consumer:
        data = None

        try:
            # Read message and get the data (dict).
            data = read_message(message=message)

        except Exception as error:  # pylint: disable=broad-except
            tries += 1
            logger.error("Consumer could not read message due to %s.", error)

            # Exit if number of tries exceeds the number of max read tries.
            if tries > MAX_READ_TRIES:
                sys.exit(1)

        finally:
            if data is not None:
                # Send the data to PostgreSQL server.
                insert_data(engine=engine, data=data)
