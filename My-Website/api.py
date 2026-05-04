from flask import Blueprint, request, jsonify
from database import db, User, Manager, Teacher, Student
from werkzeug.security import generate_password_hash, check_password_hash
import re

api_bp = Blueprint("api", __name__)


# CHECK PASSWORD
def check_password_format(password):
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


# CHECK EMAIL
def check_email_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True
    return False


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
    
    phone_number = data.get("phone_number")
    birth_date = data.get("birth_date")
    address = data.get("address")
    grade_level = data.get("grade_level")
    score = data.get("score")
    
    if not first_name or not last_name or not role or not email or not password:
        return jsonify({
            "status": "fail",
            "msg": "fields must not be empty"
        }), 400
    
    if role not in roles:
        return jsonify({
            "status": "fail",
            "msg": "enter correct role."
        }), 400
    
    if not check_password_format(password):
        return jsonify({
            "status": "fail",
            "msg": "Password must contain capital letter, small letter, number and special character."
        }), 400
    
    if not check_email_format(email):
        return jsonify({
            "status": "fail",
            "msg": "Invalid email format."
        }), 400
    
    if role == "student" and not grade_level:
        return jsonify({
            "status": "fail",
            "msg": "grade_level is required for students."
        }), 400
    
    existing_user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()
    if existing_user:
        return jsonify({
            "status": "fail",
            "msg": "Email already exists."
        }), 409

    hashed_password = generate_password_hash(password)
    
    new_user = User(
        first_name=first_name,
        last_name=last_name,
        role=role,
        email=email,
        password=hashed_password
    )
    
    db.session.add(new_user)
    db.session.flush()
    
    if role == "student":
        student = Student(
            user_id=new_user.id,
            phone_number=phone_number,
            birth_date=birth_date,
            address=address,
            score=score,
            grade_level=grade_level
        )
        db.session.add(student)
        
    elif role == "teacher":
        teacher = Teacher(
            user_id=new_user.id,
            phone_number=phone_number,
            birth_date=birth_date,
            address=address
        )
        db.session.add(teacher)
        
    elif role == "manager":
        manager = Manager(
            user_id=new_user.id,
            phone_number=phone_number,
            birth_date=birth_date,
            address=address
        )
        db.session.add(manager)
    
    db.session.commit()
    
    return jsonify({
        "status": "successful",
        "msg": f"{role} created successfully.",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "firstname": new_user.first_name,
            "lastname": new_user.last_name,
            "role": new_user.role
        }
    }), 201
    

    