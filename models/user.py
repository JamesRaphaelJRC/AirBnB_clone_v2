#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base, Column, String, relationship


class User(BaseModel, Base):
    """ This class defines a user by various attributes and maps them to
        a database table
    """
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship('Place', back_populates='user',
                          cascade='all, delete')
    reviews = relationship('Review', back_populates='user',
                           cascade='all, delete')
