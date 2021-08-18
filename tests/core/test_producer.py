"""Test the functions in producer."""

from kafka.producer.kafka import KafkaProducer
from src.core.producer import get_producer
from src.core.utilities.constants import CERT_FOLDER, SERVICE_URI, TOPIC_NAME


def test_get_producer():
    """Test getting a producer."""

    producer = get_producer(cert_folder=CERT_FOLDER, service_uri=SERVICE_URI)
    assert isinstance(producer, KafkaProducer)
