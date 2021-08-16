import uuid
from faker import Faker


def unique_id() -> uuid:
    """
    Get a universally unique identifier (UUID).

    :rtype: uuid
    """
    return uuid.uuid4()


def person() -> dict:
    """
    Generate data for a person with faker.

    :rtype: dict
    """
    fake = Faker()

    data = {
        "id": str(unique_id()),
        "name": fake.unique.name(),
        "address": fake.address(),
        "phone_number": fake.unique.phone_number(),
        "vaccinated": fake.unique.boolean()
    }
    return data
