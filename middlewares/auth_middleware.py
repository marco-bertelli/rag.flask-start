from functools import wraps
from flask import current_app
from flask import request

import jwt

from mongodb.index import getUserById


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return validate_user_token(f, False, *args, **kwargs)
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

    return decorated


def user_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return validate_user_token(f, True, *args, **kwargs)
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

    return decorated


def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return validate_admin_token(f, False, *args, **kwargs)
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

    return decorated


def validate_admin_token(f, return_user, *args, **kwargs):
    token = None

    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]

    if not token:
        return {
            "message": "Authentication Token is missing!",
            "data": None,
            "error": "Unauthorized"
        }, 401

    data = jwt.decode(
        token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

    current_user = getUserById(data["id"])

    if current_user is None:
        return {
            "message": "Invalid Authentication token!",
            "data": None,
            "error": "Unauthorized"
        }, 401

    if not current_user["isEnabled"]:
        return {
            "message": "Invalid Authentication user!",
            "data": None,
            "error": "Forbidden"
        }, 403
    
    if current_user["role"] != "admin":
        return {
            "message": "Invalid Authentication user!",
            "data": None,
            "error": "Forbidden"
        }, 403

    if return_user:
        return f(current_user, *args, **kwargs)

    return f(*args, **kwargs)


def validate_user_token(f, return_user, *args, **kwargs):
    token = None

    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]

    if not token:
        return {
            "message": "Authentication Token is missing!",
            "data": None,
            "error": "Unauthorized"
        }, 401

    data = jwt.decode(
        token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

    current_user = getUserById(data["id"])

    if current_user is None:
        return {
            "message": "Invalid Authentication token!",
            "data": None,
            "error": "Unauthorized"
        }, 401

    if not current_user["isEnabled"]:
        return {
            "message": "Invalid Authentication user!",
            "data": None,
            "error": "Forbidden"
        }, 403

    if return_user:
        return f(current_user, *args, **kwargs)

    return f(*args, **kwargs)
