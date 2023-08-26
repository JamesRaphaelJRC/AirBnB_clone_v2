#!/usr/bin/python3
"""This module instantiates the storage object based on environment."""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.state import State
from models.place import Place
from models.review import Review


if getenv("HBNB_TYPE_STORAGE") == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()

__all__ = ['storage', 'BaseModel', 'User', 'Amenity', 'City', 'State', 'Place',
           'Review']
