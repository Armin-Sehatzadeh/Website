from flask import request, jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from database import db, Teacher
from decorators import role_required

teacher_bp = Blueprint("teacher_bp", __name__, url_prefix="/api/teacher")


# TEACHER PROFILE INFO
@teacher_bp.get("/profile")
@jwt_required()
@role_required("teacher")
def teacher_profile():
    
    user_id = get_jwt_identity()
    teacher = db.session.execute(
        db.select(Teacher).where(Teacher.user_id == user_id)
        ).scalar_one_or_none() 
    
    if not teacher:
        return jsonify({
            "status": "fail",
            "msg": "Teacher not found"            
        }), 404

    return jsonify({
        "first_name": teacher.first_name,
        "last_name": teacher.last_name,       
        "phone_number": teacher.phone_number,
        "birth_date": teacher.birth_date,
        "address": teacher.address,
    }), 200
    

# EDIT TEACHER PROFILE    
@teacher_bp.patch("/profile")
@jwt_required()
@role_required("teacher")
def edit_profile():
    
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    teacher = db.session.execute(
        db.select(teacher).where(teacher.user_id == user_id)
        ).scalar_one_or_none()
    
    if not teacher:
        return jsonify({
            "status": "fail",
            "msg": "teacher not found"            
        }), 404

    allowed_fields = [
        "phone_number",
        "birth_date",
        "address",
    ]

    for field in allowed_fields:
        if field in data:

            if data[field] is None or str(data[field]).strip() == "":
                return jsonify({
                    "status": "fail",
                    "msg": f"{field} cannot be empty".title()
                }), 400

            setattr(teacher, field, data[field])

    db.session.commit()
    
    return jsonify({
        "status": "success",
        "msg": "Profile updated successfully"
    }), 200