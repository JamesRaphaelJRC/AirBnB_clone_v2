#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base, Column, Integer, String,\
        relationship


class State(BaseModel, Base):
    """Defines the State class of the HBNB project"""
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship('City', back_populates="state",
                          cascade="all, delete")

    @property
    def cities(self):
        """propery decorator for cities attribute"""
        from models import getenv

        if getenv("HBNB_TYPE_STORAGE") == 'db':
            return self.cities

        from models import storage
        from models.city import City

        city_inst = storage.all(City)
        match_cities = []
        for key, obj in city_inst.items():
            if self.id == obj.state_id:
                match_cities.append(obj)
        return match_cities
