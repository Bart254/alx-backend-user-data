#!usr/bin/env python3
"""Authentication module
"""
import bcrypt
import uuid
from db import DB
from typing import (TypeVar, Optional)
from sqlalchemy.orm.exc import NoResultFound


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
