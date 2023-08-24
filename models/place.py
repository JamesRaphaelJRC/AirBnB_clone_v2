#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base, Column, String, Integer, Float,\
        ForeignKey, relationship


class Place(BaseModel, Base):
    """ Represents A place to stay and maps it's properties to a database
        table
    """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    user = relationship("User", back_populates="places")
    cities = relationship("City", back_populates="places")
    reviews = relationship("Review", backref="place", cascade="delete")

    @property
    def reviews(self):
        """propery decorator for reviews attribute"""
        from models import getenv

        if getenv("HBNB_TYPE_STORAGE") == 'db':
            return self.reviews

        from models import storage
        from models.review import Review

        review_inst = storage.all(Review)
        match_reviews = []
        for key, obj in review_inst.items():
            if self.id == obj.place_id:
                match_reviews.append(obj)
        return match_reviews
