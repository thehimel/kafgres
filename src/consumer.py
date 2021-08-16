"""
Module for Consumer.
"""

import sys
import json
from kafka import errors, KafkaConsumer
from constants import CERT_FOLDER, SERVICE_URI, TOPIC_NAME, MAX_READ_TRIES
from logger import get_logger

logger = get_logger()


def consume_message(cert_folder=CERT_FOLDER,
                    service_uri=SERVICE_URI,
                    topic_name=TOPIC_NAME):
    """
    Consumer messages from Kafka.

    Arguments:
        cert_folder (str): Path to the directory where keys are stored.
            Default: Fetched from environment variable 'KAFKA_CERT_FOLDER'.
        service_uri (str): 'host[:port]' string of the Kafka service.
            Default: Fetched from environment variable 'KAFKA_SERVICE_URI'.
        topic_name (str): Name of the topic.
            Default: Fetched from environment variable 'KAFKA_TOPIC_NAME'.

    Returns:
        None
    """

    try:
        """
        auto_offset_reset="earliest" to read the old messages.
        Important Note: client_id and group_id are arbitrary and
            required to avoid reading the messages again.
        """

        consumer = KafkaConsumer(
            topic_name,
            auto_offset_reset="earliest",
            client_id="kafka-client-1",
            group_id="kafka-group-1",
            bootstrap_servers=service_uri,
            security_protocol="SSL",
            ssl_cafile=cert_folder+"/ca.pem",
            ssl_certfile=cert_folder+"/service.cert",
            ssl_keyfile=cert_folder+"/service.key",
            value_deserializer=lambda v: json.loads(v.decode('ascii')),
            key_deserializer=lambda v: json.loads(v.decode('ascii')),
        )

    except errors.NoBrokersAvailable:
        logger.error("Producer setup failed as no broker is available.")
        sys.exit(1)

    except Exception as error:  # pylint: disable=broad-except
        logger.error("Consumer setup failed due to %s.", error)
        sys.exit(1)

    tries = 0

    for message in consumer:
        try:
            logger.info("Received: %s:%d:%d: key=%s value=%s" % (
                message.topic,
                message.partition,
                message.offset,
                message.key,
                message.value
            ))

        except Exception as error:  # pylint: disable=broad-except
            tries += 1
            logger.error("Consumer could not read message due to %s.", error)

            # Exit if number of tries exceeds the number of max read tries.
            if tries > MAX_READ_TRIES:
                sys.exit(1)


if __name__ == "__main__":
    consume_message()
