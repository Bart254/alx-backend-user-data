#!usr/bin/env python3
"""Authentication module
"""
import bcrypt
import uuid
from db import DB
from typing import (TypeVar, Optional)
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """returns salted hash of password

    Args
        password(str): password string

    Returns:
        bytes: encrypted password
    """
    password_encoded = password.encode()
    hashed_password = bcrypt.hashpw(password_encoded, bcrypt.gensalt())
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ saves user to database
        Args:
            email(str): user's email
            password(str): user's password

        Returns:
            User: user object that has been created
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_pw = _hash_password(password).decode()
            user = self._db.add_user(email, hashed_pw)
            return user
