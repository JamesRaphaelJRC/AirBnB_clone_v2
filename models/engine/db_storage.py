#!/usr/bin/python3
''' Defines a new storage engine - a database '''
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base, BaseModel
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review


class DBStorage:
    ''' Represents our database storage engine '''
    __engine = None
    __sesssion = None

    def __init__(self):
        ''' Initializes the new storage engine'''
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format
                                      (getenv('HBNB_MYSQL_USER'),
                                       getenv('HBNB_MYSQL_PWD'),
                                       getenv('HBNB_MYSQL_HOST'),
                                       getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') is 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        ''' Queries on the current database session all objects depending on
            the class name 'cls' and querie and returns a dictionary in this
            format:
                <class name>.<object id> = value(the object)
        '''
        objects = []
        if cls is None:
            objects.extend(self.__session.query(User).all())
            objects.extend(self.__session.query(State).all())
            objects.extend(self.__session.query(City).all())
            objects.extend(self.__session.query(Amenity).all())
            objects.extend(self.__session.query(Place).all())
            objects.extend(self.__session.query(Review).all())
        else:
            if type(cls) is str:
                objCls = eval(cls)

            objects = self.__session.query(objCls).all()

        return {"{}.{}".format(type(obj).__name__, obj.id): obj for obj in
                objects}

    def new(self, obj):
        ''' Adds the object to the current database session '''
        self.__session.add(obj)

    def save(self):
        ''' Commit all changes to the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        ''' Deletes from the current database session obj if not None.'''
        if obj not None:
            self.__session.delete(obj)

    def reload(self):
        ''' Create all tables in the databases.'''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
