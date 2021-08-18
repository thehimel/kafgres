"""Test the functions in consumer."""

from kafka.consumer import KafkaConsumer
from src.core.consumer import get_consumer
from src.core.utilities.constants import CERT_FOLDER, SERVICE_URI, TOPIC_NAME


def test_get_consumer():
    """Test getting a consumer."""

    consumer = get_consumer(
        cert_folder=CERT_FOLDER, service_uri=SERVICE_URI, topic_name=TOPIC_NAME
    )
    assert isinstance(consumer, KafkaConsumer)
