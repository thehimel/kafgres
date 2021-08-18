"""Test the functions in producer."""

from kafka.producer.kafka import KafkaProducer
from src.core.producer import get_producer, send_message
from src.core.utilities.constants import CERT_FOLDER, SERVICE_URI, TOPIC_NAME, MAX_WAIT
from src.core.utilities.data import person


def test_get_producer():
    """Test getting a producer."""

    producer = get_producer(cert_folder=CERT_FOLDER, service_uri=SERVICE_URI)
    assert isinstance(producer, KafkaProducer)


def test_send_message():
    producer = get_producer(cert_folder=CERT_FOLDER, service_uri=SERVICE_URI)

    producer = send_message(
        producer=producer,
        topic_name=TOPIC_NAME,
        data=person(),
        max_wait=MAX_WAIT,
    )[0]

    assert isinstance(producer, KafkaProducer)
