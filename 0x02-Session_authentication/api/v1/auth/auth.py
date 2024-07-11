#!/usr/bin/env python3
""" Authorization module
"""
import os
import re
from flask import request
from typing import (List, TypeVar)


class Auth:
    """ Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if a route requires authentication

        Args:
            path(str): route to be checked
            excluded_paths(List[str]): routes excluded from authentication

        Returns:
            bool: False if no authentication required, otherwise True
        """
        if not path or not excluded_paths or not len(excluded_paths):
            return True

        for route in excluded_paths:
            if route.endswith('*'):
                pattern = route + '.*'
            else:
                pattern = route + '?'
            if re.fullmatch(pattern, path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ validates all requests

        Args:
            request: request object

        Returns:
            Optional[str]: Value of the authorization otherwise None
        """
        if request is None:
            return None
        auth_value = request.headers.get('Authorization')
        return auth_value

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request """
        if request is None:
            return None

        _my_session_id = os.getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)
