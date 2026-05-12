from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db, Student
from decorators import role_required

student_bp = Blueprint("student_bp", __name__, url_prefix="/api/student")


# GET SCORE
@student_bp.get("/score")
@jwt_required()
@role_required("student")
def get_score():
    user_id = get_jwt_identity()

    student = db.session.execute(
        db.select(Student).where(Student.user_id == user_id)
    ).scalar_one_or_none()

    if not student:
        return jsonify({
            "status": "fail",
            "msg": "Student not found"
        }), 404

    return jsonify({
        "first_name": student.user.first_name,
        "last_name": student.user.last_name,
        "score": student.score,
        "grade_level": student.grade_level
    }), 200


# STUDENT PROFILE INFO
@student_bp.get("/profile")
@jwt_required()
@role_required("student")
def student_profile():
    
    user_id = get_jwt_identity()
    student = db.session.execute(
        db.select(Student).where(Student.user_id == user_id)
        ).scalar_one_or_none() 
    
    if not student:
        return jsonify({
            "status": "fail",
            "msg": "Student not found"            
        }), 404

    return jsonify({
        "first_name": student.user.first_name,
        "last_name": student.user.last_name,       
        "phone_number": student.phone_number,
        "birth_date": str(student.birth_date),
        "address": student.address,
        "grade_level": student.grade_level,
        "score": student.score
    }), 200
    
    
# EDIT STUDENT PROFILE    
@student_bp.patch("/profile")
@jwt_required()
@role_required("student")
def edit_profile():
    
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    student = db.session.execute(
        db.select(Student).where(Student.user_id == user_id)
        ).scalar_one_or_none()
    
    if not student:
        return jsonify({
            "status": "fail",
            "msg": "Student not found"            
        }), 404

    allowed_fields = [
        "phone_number",
        "birth_date",
        "address",
        "grade_level"
    ]

    for field in allowed_fields:
        if field in data:

            if data[field] is None or str(data[field]).strip() == "":
                return jsonify({
                    "status": "fail",
                    "msg": f"{field} cannot be empty".title()
                }), 400

            setattr(student, field, data[field])

    db.session.commit()
    
    return jsonify({
        "status": "success",
        "msg": "Profile updated successfully"
    }), 200