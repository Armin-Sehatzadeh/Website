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

    