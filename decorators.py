from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt


def role_required(role):

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):

            jwt_data = get_jwt()
            user_role = jwt_data.get("role")

            if user_role != role:
                return jsonify({"msg": "Access denied"}), 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper
