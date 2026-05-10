from flask import request, Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from decorators import role_required
from database import db, Manager, Student, Teacher

manager_bp = Blueprint("manager_bp", __name__, url_prefix="/api/manager")

def get_current_manager():
    user_id = get_jwt_identity()
    
    return db.session.execute(
        db.select(Manager).where(Manager.user_id == user_id)
        ).scalar_one_or_none()


# MANAGER PROFILE
@manager_bp.get("/profile")
@jwt_required()
@role_required("manager")
def manager_profile():
    
    manager = get_current_manager()
    if not manager:
        return jsonify({"msg": "Manager not found"}), 404

    return jsonify({
        "first_name": manager.user.first_name,
        "last_name": manager.user.last_name,
        "phone_number": manager.phone_number,
        "address": manager.address,
        "birth_date": str(manager.birth_date)
    }), 200


# EDIT MANAGER PROFILE
@manager_bp.patch("/profile")
@jwt_required()
@role_required("manager")
def edit_profile():
    
    manager = get_current_manager()
    if not manager:
        return jsonify({"msg": "Manager not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"msg": "Data not found"}), 400
    
    allowed = ["phone_number", "address"]

    for field in allowed:
        if field in data:
            setattr(manager, field, data[field])

    db.session.commit()
    return jsonify({"msg": "Profile updated"}), 200


# EDIT TEACHER PROFILE
@manager_bp.patch("/teacher/<int:teacher_id>")
@jwt_required()
@role_required("manager")
def edit_teacher(teacher_id):

    teacher = db.session.get(Teacher, teacher_id)
    if not teacher:
        return jsonify({"msg": "Teacher not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"msg": "No data provided"}), 400

    allowed = ["phone_number", "address"]

    for field in allowed:
        if field in data:
            setattr(teacher, field, data[field])

    db.session.commit()
    return jsonify({"msg": "Teacher updated"}), 200


# EDIT STUDENT PROFILE
@manager_bp.patch("/student/<int:student_id>")
@jwt_required()
@role_required("manager")
def edit_student(student_id):

    student = db.session.get(Student, student_id)

    if not student:
        return jsonify({"msg": "Student not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"msg": "No data provided"}), 400

    allowed = [
        "phone_number",
        "birth_date",
        "address",
        "grade_level",
        "score"
    ]

    for field in allowed:
        if field in data:
            setattr(student, field, data[field])

    db.session.commit()

    return jsonify({"msg": "Student updated"}), 200


# ASSIGN STUDENT TO TEACHER
@manager_bp.post("/assign-student")
@jwt_required()
@role_required("manager")
def assign_student():

    data = request.get_json()

    student = db.session.get(Student, data.get("student_id"))
    teacher = db.session.get(Teacher, data.get("teacher_id"))

    if not student or not teacher:
        return jsonify({"msg": "Student or Teacher not found"}), 404

    student.teacher_id = teacher.id

    db.session.commit()

    return jsonify({"msg": "Student assigned"}), 200


# GET STUDENTS LIST
@manager_bp.get("/students")
@jwt_required()
@role_required("manager")
def get_students():
    students = Student.query.all()

    result = []
    for s in students:
        result.append({
            "id": s.id,
            "first_name": s.user.first_name,
            "last_name": s.user.last_name,
            "phone": s.phone,
            "grade": s.grade,
            "score": s.score,
            "teacher_id": s.teacher_id
        })

    return jsonify(result), 200


# GET TEACHER LIST
@manager_bp.get("/teachers")
@jwt_required()
@role_required("manager")
def get_teachers():
    teachers = Teacher.query.all()

    result = []
    for t in teachers:
        result.append({
            "id": t.id,
            "first_name": t.user.first_name,
            "last_name": t.user.last_name,
            "phone": t.phone,
            "students_count": len(t.students)
        })

    return jsonify(result), 200


