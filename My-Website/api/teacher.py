from flask import request, jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from database import db, Teacher, Student
from decorators import role_required

teacher_bp = Blueprint("teacher_bp", __name__, url_prefix="/api/teacher")


def get_current_teacher():
    user_id = get_jwt_identity()
    teacher = db.session.execute(
        db.select(Teacher).where(Teacher.user_id == user_id)
    ).scalar_one_or_none()

    return teacher


def get_student(student_id):
    return db.session.execute(
        db.select(Student).where(Student.id == student_id)
    ).scalar_one_or_none()


def check_score(score):
    if score is None:
        return jsonify({"status": "fail", "msg": "Score required"}), 400

    if not (0 <= score <= 20):
        return jsonify({
            "status": "fail",
            "msg": "Score must be between 0 and 20."
        }), 400


def validate_teacher_student(teacher, student):
    if not teacher:
        return jsonify({"status": "fail", "msg": "Teacher not found"}), 404

    if not student:
        return jsonify({"status": "fail", "msg": "Student not found"}), 404

    if student.teacher_id != teacher.id:
        return jsonify({"status": "fail", "msg": "Not your student"}), 403
    

# TEACHER PROFILE
@teacher_bp.get("/profile")
@jwt_required()
@role_required("teacher")
def teacher_profile():

    teacher = get_current_teacher()

    if not teacher:
        return jsonify({"status": "fail", "msg": "Teacher not found"}), 404

    return jsonify({
        "first_name": teacher.user.first_name,
        "last_name": teacher.user.last_name,
        "phone_number": teacher.phone_number,
        "birth_date": teacher.birth_date,
        "address": teacher.address,
    }), 200


# EDIT PROFILE
@teacher_bp.patch("/profile")
@jwt_required()
@role_required("teacher")
def edit_profile():

    teacher = get_current_teacher()
    if not teacher:
        return jsonify({"status": "fail", "msg": "Teacher not found"}), 404

    data = request.get_json() or {}

    allowed = ["phone_number", "birth_date", "address"]

    for field in allowed:
        if field in data and data[field]:
            setattr(teacher, field, data[field])

    db.session.commit()
    return jsonify({"status": "success", "msg": "Profile updated"}), 200


# GET STUDENTS
@teacher_bp.get("/students")
@jwt_required()
@role_required("teacher")
def get_students():

    teacher = get_current_teacher()
    if not teacher:
        return jsonify({"status": "fail", "msg": "Teacher not found"}), 404

    students = db.session.execute(
        db.select(Student).where(Student.teacher_id == teacher.id)
    ).scalars().all()

    students_list = []
    for s in students:
        students_list.append({
            "id": s.id,
            "name": f"{s.user.first_name} {s.user.last_name}",
            "grade_level": s.grade_level,
            "score": s.score
        })

    return jsonify({"status": "success", "students": students_list}), 200


# SET SCORE
@teacher_bp.post("/score/<int:student_id>")
@jwt_required()
@role_required("teacher")
def set_score(student_id):

    data = request.get_json() or {}
    score = data.get("score")

    err = check_score(score)
    if err:
        return err

    teacher = get_current_teacher()
    student = get_student(student_id)

    err = validate_teacher_student(teacher, student)
    if err:
        return err

    student.score = score
    db.session.commit()

    return jsonify({"status": "success", "msg": "Score set"}), 200


# EDIT SCORE
@teacher_bp.patch("/score/<int:student_id>")
@jwt_required()
@role_required("teacher")
def edit_score(student_id):

    data = request.get_json() or {}
    score = data.get("score")

    err = check_score(score)
    if err:
        return err

    teacher = get_current_teacher()
    student = get_student(student_id)

    err = validate_teacher_student(teacher, student)
    if err:
        return err

    student.score = score
    db.session.commit()

    return jsonify({"status": "success", "msg": "Score updated"}), 200


# DELETE SCORE
@teacher_bp.delete("/score/<int:student_id>")
@jwt_required()
@role_required("teacher")
def delete_score(student_id):

    teacher = get_current_teacher()
    student = get_student(student_id)

    err = validate_teacher_student(teacher, student)
    if err:
        return err

    student.score = None
    db.session.commit()

    return jsonify({"status": "success", "msg": "Score deleted"}), 200
