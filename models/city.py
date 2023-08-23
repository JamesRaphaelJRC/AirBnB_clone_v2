#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base, Column, String, Integer,\
        ForeignKey, relationship


class City(BaseModel, Base):
    """ Defines the City class with two attributes and a relationship attribute
        with State class.
    """
    __tablename__ = 'cities'

    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    name = Column(String(128), nullable=False)
