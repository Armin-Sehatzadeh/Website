from flask import Blueprint, request, jsonify
from database import db, User
from werkzeug.security import generate_password_hash, check_password_hash

api_bp = Blueprint("api", __name__)

# LOGIN API
@api_bp.post("/login")
def login_api():
    data = request.json

    email = data.get("email")
    password = data.get("password")


    if not email or not password:
        return jsonify({
            "status": "fail",
            "msg": "email or password missing."
        }), 400
    
    
    result = db.session.execute(db.select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        return jsonify({
            "status": "fail",
            "msg": "email or password is incorrect."
        }), 401
        
    
    if not check_password_hash(user.password, password):
        return jsonify({
            "status": "fail",
            "msg": "email or password is incorrect."
        }), 401


    return jsonify({
    "status": "successful",
    "msg": "you are logged in.",
    "user": {
        "id": user.id,
        "email": user.email,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "role": user.role
    }
}), 200


