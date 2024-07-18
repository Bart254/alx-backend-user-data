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


def _generate_uuid() -> uuid:
    """ generates a unique user id """
    return uuid.uuid4()


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

    def valid_login(self, email: str, password: str) -> bool:
        """ validates a user
        Args:
            email(str): user's email
            password(str): user's password

        Returns:
            bool: True if email and password match, otherwise False
        """
        try:
            user = self._db.find_user_by(email=email)
            password = password.encode()
            is_valid = bcrypt.checkpw(password, user.hashed_password.encode())
            return is_valid

        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ creates a session for user """
        try:
            user = self._db.find_user_by(email=email)
            new_session_id = str(_generate_uuid())
            self._db.update_user(user.id, session_id=new_session_id)
            return new_session_id

        except NoResultFound:
            None
