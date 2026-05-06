from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from database import db, Student
from decorators import role_required
from flask_jwt_extended import get_jwt_identity

student_bp = Blueprint("student_bp", __name__, url_prefix="/api/student")


@student_bp.get("/score")
@jwt_required()
@role_required("student")
def get_score():
    user_id = get_jwt_identity()

    student = db.session.execute(
        db.select(Student).where(Student.user_id == user_id)
    ).scalar_one_or_none()

    if not student:
        return jsonify({"msg": "Student not found"}), 404

    return jsonify({
        "score": student.score,
        "grade_level": student.grade_level
    }), 200
