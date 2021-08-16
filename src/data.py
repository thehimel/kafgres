import uuid
from faker import Faker


def unique_id():
    """
    Get a universally unique identifier (UUID).

    Returns:
        uuid
    """
    return uuid.uuid4()


def person():
    """
    Generate data for a person with faker.

    Returns:
        tuple
    """

    fake = Faker()

    message = {
        "id": str(unique_id()),
        "name": fake.unique.name(),
        "address": fake.address(),
        "phone_number": fake.unique.phone_number(),
        "vaccinated": fake.unique.boolean()
    }

    key = {'id': message["id"]}
    return message, key
