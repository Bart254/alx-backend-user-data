#!/usr/bin/env python3
""" Session authentication api module """
import os
from api.v1.views import app_views
from flask import (abort, jsonify, request)


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def session_view():
    """ handler for session view api """
    from models.user import User
    from api.v1.app import auth
    email = request.form.get('email')
    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get("password")
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if user is None or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = user[0]
    if (not user.is_valid_password(password)):
        return jsonify({"error": "wrong password"}), 401
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    _my_session_id = os.getenv('SESSION_NAME')
    response.set_cookie(_my_session_id, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ logs out a user session """
    from api.v1.app import auth
    if (not auth.destroy_session(request)):
        abort(404)
    else:
        return jsonify({}), 200
