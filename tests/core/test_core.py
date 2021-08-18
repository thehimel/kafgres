"""Integration test for core"""

import time
from src.core.producer import get_producer, send_message
from src.core.utilities.constants import CERT_FOLDER, SERVICE_URI, TOPIC_NAME
from src.core.utilities.data import person
from src.core.consumer import get_consumer


def test_core():
    producer = get_producer(cert_folder=CERT_FOLDER, service_uri=SERVICE_URI)
    data = person()
    send_message(
        producer=producer,
        topic_name=TOPIC_NAME,
        data=data,
        max_wait=0,
    )

    consumer = get_consumer(
        cert_folder=CERT_FOLDER,
        service_uri=SERVICE_URI,
        topic_name=TOPIC_NAME,
        consumer_timeout_ms=5000,
    )

    # Consumer will terminate if no message is received within 5000 ms.
    for message in consumer:
        if data[0]["id"] == message.value["id"]:
            assert True
            break
