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


    