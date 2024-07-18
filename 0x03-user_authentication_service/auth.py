#!usr/bin/env python3
"""Auth module"""
import bcrypt
import uuid
from db import DB
from typing import (TypeVar, Optional)
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """ saves user to database
        Args:
            email(str): user's email
            password(str): user's password

        Returns:
            User: user object that has been created
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_pw = self._db._hash_password(password)
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
            is_valid = bcrypt.checkpw(password, user.hashed_password)
            return is_valid

        except (Exception):
            return False

    def _generate_uuid(self) -> uuid:
        """ generates a unique user id """
        return uuid.uuid4()

    def create_session(self, email: str) -> str:
        """ creates a session for user """
        try:
            user = self._db.find_user_by(email=email)
            new_session_id = str(self._generate_uuid())
            self._db.update_user(user.id, session_id=new_session_id)
            return new_session_id

        except NoResultFound:
            None

    def get_user_from_session_id(self, session_id: str) -> Optional[
            TypeVar('User')]:
        """returns user from session_id """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user

        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """ destroy's a user session """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """updates user's reset token"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = str(self._generate_uuid())
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token

        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """update's user password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            password = password.encode()
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            self._db.update_user(user.id, hashed_password=hashed_password,
                                 reset_token=None)

        except NoResultFound:
            raise ValueError
