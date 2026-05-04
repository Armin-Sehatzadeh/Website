from flask import Blueprint, request, jsonify
from database import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import re

api_bp = Blueprint("api", __name__)


# CHECK PASSWORD
def check_pass(password):
    if len(password) < 8:
        return False
    
    if not re.search(r'[A-Z]', password):
        return False

    if not re.search(r'[a-z]', password):
        return False

    if not re.search(r'[0-9]', password):
        return False
    
    if not re.search(r'[^A-Za-z0-9]', password):
        return False
    
    return True


# LOGIN API
@api_bp.post("/login")
def login_api():
    data = request.json

    email = data.get("email")
    password = data.get("password")


    if not email or not password:
        return jsonify({
            "status": "fail",
            "msg": "Email or password missing."
        }), 400
    
    
    result = db.session.execute(db.select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        return jsonify({
            "status": "fail",
            "msg": "Email or password is incorrect."
        }), 401
        
    
    if not check_password_hash(user.password, password):
        return jsonify({
            "status": "fail",
            "msg": "Email or password is incorrect."
        }), 401


    return jsonify({
    "status": "successful",
    "msg": "Logged in.",
    "user": {
        "id": user.id,
        "email": user.email,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "role": user.role
    }
}), 200


@api_bp.post("/sign-in")
def sign_in_api():
    data = request.json
    roles = ["student", "teacher", "manager"]
    
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    role = data.get("role")
    email = data.get("email")
    password = data.get("password")
    
    if not first_name or not last_name or not role or not email or not password:
        return jsonify({
            "status": "fail",
            "msg": "Fields must not be empty."
        }), 400
    
    if role not in roles:
        return jsonify({
            "status": "fail",
            "msg": "Enter correct role."
        })
    
    if not check_pass(password):
        return jsonify({
            "status": "fail",
            "msg": "Password must contain capital letter, small letter, number and special character."
        }), 400

    