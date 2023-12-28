from functools import wraps
from flask import request

import requests
import os


def validate_re_captcha_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return validate_captcha_token(f, *args, **kwargs)
        except Exception as e:
            print(e)
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

    return decorated


def validate_captcha_token(f, *args, **kwargs):
    token = None

    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]

    if not token:
        return {
            "message": "Captcha Token is missing!",
            "data": None,
            "error": "Unauthorized"
        }, 401

    response = requests.post(
        url="https://www.google.com/recaptcha/api/siteverify",
        params={
            'secret': os.getenv("RECAPTCHA_SECRET_KEY"),
            'response': token
        }
    )

    json_result = response.json()

    if not json_result["success"]:
        return {
            "message": "Captcha Token is invalid!",
            "data": None,
            "error": "Unauthorized"
        }, 401

    return f(*args, **kwargs)
