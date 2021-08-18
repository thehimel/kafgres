"""Integration test for core."""

from src.core.producer import get_producer, send_message
from src.core.utilities.constants import (
    CERT_FOLDER,
    SERVICE_URI,
    TOPIC_NAME,
    PG_SERVICE_URI,
)
from src.core.utilities.data import person
from src.core.insert import init_db, insert_data, get_data, vaccination_data
from src.core.consumer import get_consumer, read_message


def test_core():
    """Integration test for producer, consumer, data insertion
    and data retrieval."""

    producer = get_producer(cert_folder=CERT_FOLDER, service_uri=SERVICE_URI)

    # person() returns (message, key)
    data = person()
    data_id = data[0]["id"]
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
        consumer_timeout_ms=10000,
    )

    msg = None

    # Consumer will terminate if no message is
    #   received within consumer_timeout_ms.
    for message in consumer:
        if data_id == message.value["id"]:
            msg = message
            break

    if msg:
        msg = read_message(msg)
        engine = init_db(PG_SERVICE_URI)
        insert_data(engine=engine, data=msg)
        fetched_data = get_data(engine=engine, data_id=data_id)
        assert vaccination_data(data[0]).id == fetched_data.id
