#!/usr/bin/env python3
""" Expiring session module """
import os
from api.v1.auth.session_auth import SessionAuth
from datetime import (datetime, timedelta)


class SessionExpAuth(SessionAuth):
    """ class session expiration authentication """
    def __init__(self):
        """ initialization method """
        try:
            duration = os.getenv('SESSION_DURATION')
            duration = int(duration)
            self.session_duration = duration
        except (Exception):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ returns session_id for user """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ returns user id from session dictionary """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        user_id = self.user_id_by_session_id[session_id].get("user_id")
        if self.session_duration <= 0:
            return user_id

        created_at = self.user_id_by_session_id[session_id].get("created_at")
        if created_at is None:
            return None
        cur_time = datetime.now()

        if created_at + timedelta(seconds=self.session_duration) < cur_time:
            return None
        return user_id
