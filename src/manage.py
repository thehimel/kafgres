"""
Starting point of the application.
"""

import sys
from core.insert import init_db, send_data
from core.utilities.constants import PG_SERVICE_URI
from core.utilities.data import person
from core.producer import produce_messages
from core.consumer import consume_message


def insert():
    """
    Insert data to the PostgreSQL server.
    """

    db_engine = init_db(PG_SERVICE_URI)
    person_data = person()[0]
    send_data(engine=db_engine, data=person_data)


def producer():
    """
    Run the producer.
    """

    try:
        produce_messages()
    except KeyboardInterrupt:
        print("\nProducer stopped")
        sys.exit(0)


def consumer():
    """
    Run the consumer.
    """

    try:
        db_engine = init_db(PG_SERVICE_URI)
        consume_message(db_engine)
    except KeyboardInterrupt:
        print("\nConsumer stopped")
        sys.exit(0)


if __name__ == "__main__":
    tasks = {
        "producer": produce_messages(),
        "consumer": consumer,
        "insert": insert
    }

    msgs = [
        "Allowed option: argument, consumer, or insert.",
        "Only one argument must be passed.",
        "Invalid argument."
    ]

    # If the no argument is passed.
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print(msgs[1], msgs[0])
    else:
        task = sys.argv[1]

        # If an invalid argument is passed.
        if task not in tasks:
            print(msgs[2], msgs[0])
        else:
            # Run the task.
            tasks[task]()
