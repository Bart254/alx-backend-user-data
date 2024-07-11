#!/usr/bin/env python3
"""Session Authorization Module"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session authorization class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a session id for a user_id """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns user_id based on session_id """
        if session_id is None or not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """ returns user object based on session_id """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """ destroys a user session/logs out a user """
        if request is None:
            return False
        session_id = self.session_cookie(request)

        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)

        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
