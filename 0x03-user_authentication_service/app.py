#!/usr/bin/env python3
"""Flask application"""
from auth import Auth
from flask import (abort, Flask, jsonify, redirect, request, url_for)

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    """ root url """
    payload = {"message": "Bienvenue"}
    return jsonify(payload)


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ users endpoint for registration """
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        user = AUTH.register_user(email, password)
        if user:
            message = {"email": f"{user.email}",
                       "message": "user created"
                       }
            return jsonify(message)

    except ValueError:
        user_exists_message = {"message": "email already registered"}
        return jsonify(user_exists_message)


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ login handler """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401), 401

    session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}",
                        "message": "logged in"
                        })
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ logs user out of a session """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('index'))
    abort(403), 403


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """returns the profile of a user"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        message = {"email": f"{user.email}"}
        return jsonify(message), 200
    abort(403), 403


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ reset_password handler """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        message = {"email": f"{email}",
                   "reset_token": f"{reset_token}"
                   }
        return jsonify(message), 200

    except ValueError:
        abort(403), 403


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """updates user password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('password')
    try:
        AUTH.update_password(reset_token, new_password)
        message = {"email": f"{email}",
                   "message": "Password updated"
                   }
        return jsonify(message)

    except ValueError:
        abort(403), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
