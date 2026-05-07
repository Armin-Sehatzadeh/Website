from flask import request, jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from database import db, Teacher, Student
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
    

# TEACHERS STUDENTS
@teacher_bp.get("/students")
@jwt_required()
@role_required("teacher")
def get_students():

    user_id = get_jwt_identity()

    teacher = db.session.execute(
        db.select(Teacher).where(Teacher.user_id == user_id)
    ).scalar_one_or_none()

    if not teacher:
        return jsonify({"status": "fail", "msg": "Teacher not found"}), 404
    
    users = db.session.execute(
    db.select(Student).where(Student.teacher_id == user_id)
    ).scalars().all()
    
    students = []

    for user in users:
        students.append({
            "id": user.id,
            "name": f"{user.user.first_name} {user.user.last_name}",
            "grade_level": user.grade_level,
            "score": user.score
        })
        
    return jsonify({
        "status": "success",
        "students": students
    }), 200


# SET SCORE
@teacher_bp.post("/score/<int:student_id>")
@jwt_required()
@role_required("teacher")
def set_score(student_id):
    
    data = request.get_json() or {}
    score = data.get("score")
    
    if score is None:
        return jsonify({"status": "fail", "msg": "Score required"}), 400
    
    user_id = get_jwt_identity()

    teacher = db.session.execute(
        db.select(Teacher).where(Teacher.user_id == user_id)
    ).scalar_one_or_none()
    
    student = db.session.execute(
        db.select(Student).where(Student.id == student_id)
    ).scalar_one_or_none()
    
    if not student:
        return jsonify({"status": "fail", "msg": "Student not found"}), 404
    
    if student.teacher_id != teacher.id:
        return jsonify({"status": "fail", "msg": "Not your student"}), 403

    student.score = score
    db.session.commit()

    return jsonify({"status": "success", "msg": "Score set"}), 200

    