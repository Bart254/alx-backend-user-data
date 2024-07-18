#!/usr/bin/env python3
"""DB class module
"""
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.exc import (InvalidRequestError, NoResultFound)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import (Base, User)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ saves a user to the database
        Args:
            email(str): user's email
            hashed_password(str): user's password

        Returns:
            User(object): a user object created and saved in database
        """
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs):
        """ returns first row of users filtered by keyword args """
        if len(kwargs) != 1:
            raise InvalidRequestError

        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ updates a user's attribute
        Args:
            user_id(int): id of user to update
            kwargs(dict): key-word args containing attributes to update
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError

    def _hash_password(self, password: str) -> bytes:
        """returns salted hash of password"""
        password_encoded = password.encode()
        hashed_password = bcrypt.hashpw(password_encoded, bcrypt.gensalt())
        return hashed_password
