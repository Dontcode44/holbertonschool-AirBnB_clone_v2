#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from tokenize import String
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from models.city import City
from sqlalchemy.orm import backref
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    if getenv('HBNB_TYPE_STORAGE') == 'db':

        name = Column(String(128), nullable=False)
        cities = relationship("City", backref='state', cascade='all, delete')

    else:
        name = ""
    if models.storage != 'db':
        @property
        def cities(self):
            """ Returns the list of City
            """
            list_cities = []
            all_cities = models.storage.all(City)
            for key, city_obj in all_cities.items():
                if city_obj.state_id == self.id:
                    list_cities.append(city_obj)
            return list_cities

