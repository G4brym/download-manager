from functools import wraps

from flask import jsonify, request

from downloads.core import API_KEY


def authorizer(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if request.args.get('authorization') != API_KEY and request.headers.get('authorization') != API_KEY:
            return jsonify({"success": False, "message": "Missing authorization key"}), 401
        return func(*args, **kwargs)

    return decorated_function
