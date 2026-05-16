from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from database import db, User


def role_required(role):

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):

            user_id = get_jwt_identity()

            user = db.session.get(User, user_id)

            if not user or user.role != role:
                return jsonify({"msg": "Access denied"}), 403

            return fn(*args, **kwargs)

        return decorator

    return wrapper
