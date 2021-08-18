"""
Module to store the database models.
"""

import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from utils.constants import TABLE_NAME

Base = declarative_base()


class Vaccination(Base):
    """
    Vaccination Table
    """

    __tablename__ = TABLE_NAME

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    address = Column(String)
    phone_number = Column(String)
    vaccinated = Column(Boolean)

    @property
    def repr_dict(self):
        """
        Dictionary representation of the object.
        """

        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone_number": self.phone_number,
            "vaccinated": self.vaccinated,
        }

    def __str__(self):
        """
        String representation of the object.
        """

        return (
            f"id: {self.id}, name: {self.name}, phone_number: "
            + f"{self.phone_number}, vaccinated: {self.vaccinated}"
        )
