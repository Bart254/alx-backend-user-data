#!/usr/bin/env python3
"""Test module"""
import requests
from user import User


def register_user(email: str, password: str) -> None:
    """tests if a user is successfully registered in the database"""
    url = 'http://0.0.0.0:5000/users'
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    expected_message = {"email": f"{email}",
                        "message": "user created"
                        }
    assert response.status_code == 200
    assert response.json() == expected_message


def log_in_wrong_password(email: str, password: str) -> None:
    """tests wrong login credentials
    """
    url = 'http://0.0.0.0:5000/sessions'
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ tests correct login credentials
    """
    url = 'http://0.0.0.0:5000/sessions'
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    expected_message = {"email": f"{email}",
                        "message": "logged in"
                        }

    assert response.status_code == 200
    assert response.json() == expected_message
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    assert type(session_id) is str
    return session_id


def profile_unlogged() -> None:
    """tests a logged out user profile"""
    url = 'http://0.0.0.0:5000/profile'
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """tests a logged in user profile"""
    url = 'http://0.0.0.0:5000/profile'
    response = requests.get(url, cookies={"session_id": session_id})
    expected_message = {"email": f"{EMAIL}"}
    assert response.status_code == 200
    assert response.json() == expected_message


def log_out(session_id: str) -> None:
    """tests destroying session_id"""
    url = 'http://0.0.0.0:5000/sessions'
    response = requests.delete(url, cookies={"session_id": session_id})
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """returns reset_password token"""
    url = 'http://0.0.0.0:5000/reset_password'
    data = {"email": email}
    response = requests.post(url, data=data)
    response_json = response.json()
    reset_token = response_json.get("reset_token")
    expected_message = {"email": f"{email}",
                        "reset_token": f"{reset_token}"
                        }
    assert response.status_code == 200
    assert response_json == expected_message
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """tests successful update of user's password"""
    url = 'http://0.0.0.0:5000/reset_password'
    data = {"email": email,
            "reset_token": reset_token,
            "new_password": new_password
            }
    response = requests.put(url, data=data)
    expected_message = {"email": f"{email}",
                        "message": "Password updated"
                        }
    assert response.status_code == 200
    assert response.json() == expected_message


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
