#!/usr/bin/python3
""" Place Module for HBNB project """
from curses import meta
from importlib.metadata import metadata
from models.amenity import Amenity
from models.base_model import BaseModel
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from models.city import City
from models.engine.db_storage import DBStorage
from models.review import Review
from models.user import User
from sqlalchemy.orm import relationship
from os import getenv

from sqlalchemy import *

metadata = Base.metadata

place_amenity = Table('place_amenity', metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             nullable=False, primary_key=True),
                      Column('amenity_id', String(60), ForeignKey('amenities.id'),
                             nullable=False, primary_key=True))

class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []
        reviews = relationship("Review", backref="place")
        amenities = relationship("Amenity", secundary=place_amenity, viewonly=False)

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        if getenv("HBNB_TYPE_STORAGE") == "db":
            reviews = relationship("Review", backref='place', cascade="all, delete")
            amenities = relationship("Amenity", secondary=place_amenity,
                            viewonly=False, cascade="all, delete",
                            backref="places")
        else:
            from models import DBStorage
            @property
            def reviews(self):
                """ Returns the list of Review instances with
                    place_id equals to the current Place.id
                """
                reviews = []
                for place in DBStorage.all(Review).values():
                    if place.id == self.place_id:
                        reviews.append(place)
                return reviews

            @property
            def amenities(self):
                """ Function that returns the list of City
                instances with state_id """

                amenities_list = []
                for amenity in DBStorage.all(Amenity).values():
                    if amenity.id == self.amenity_id:
                        amenities_list.append(amenity)
                return amenities_list
 

            @amenities.setter 
            def ameninities(self, arg):
                """ Function setter amenities """
                if arg.__class__.name__ == "Amenity":
                    self.amenity_ids.append(arg)