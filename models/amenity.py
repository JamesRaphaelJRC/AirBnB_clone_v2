#!/usr/bin/python3
""" Amenity Class for HBNB project """
from models.base_model import BaseModel, Base, Column, String, relationship


class Amenity(BaseModel, Base):
    """ This defines and maps the Amenity class"""

    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary="place_amenity",
                                   back_populates="amenities")
