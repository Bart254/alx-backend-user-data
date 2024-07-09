#!/usr/bin/env python3
""" Basic Auth Module"""
import base64
from api.v1.auth.auth import Auth
from typing import (Optional, Tuple, TypeVar)


class BasicAuth(Auth):
    """ class Basic Auth"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ returns Base64 part of authorization header"""
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        try:
            string = authorization_header.split()[1]
            return string

        except (Exception):
            return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of base64 string"""
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded = base64.b64decode(
                base64_authorization_header.encode('utf-8')
                ).decode('utf-8')
            return decoded

        except (Exception):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[
            Optional[str], Optional[str]]:
        """ returns username and password from decoded header """
        if decoded_base64_authorization_header is None:
            return (None, None)

        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        user_email, password = decoded_base64_authorization_header.split(':',
                                                                         1)
        return (user_email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns user object from credentials """
        from models.user import User
        if not user_email or not isinstance(user_email, str):
            return None

        if not user_pwd or not isinstance(user_pwd, str):
            return None

        users = User.search({"email": user_email})
        if not users or len(users) != 1:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrievs current user """
        try:
            auth_str = self.authorization_header(request)
            b64_str = self.extract_base64_authorization_header(auth_str)
            decoded_str = self.decode_base64_authorization_header(b64_str)
            email, passwd = self.extract_user_credentials(decoded_str)
            user = self.user_object_from_credentials(email, passwd)
            return user

        except (Exception):
            return None
