from flask import Flask, render_template
from database import db, TokenBlocklist
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from api.auth import auth_bp
from api.student import student_bp
from api.teacher import teacher_bp
from api.manager import manager_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key"

db.init_app(app)

jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"])

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(student_bp, url_prefix="/api/student")
app.register_blueprint(teacher_bp, url_prefix="/api/teacher")
app.register_blueprint(manager_bp, url_prefix="/api/manager")


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token is not None

# ── Page Routes ──

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/student-dashboard')
def student_dashboard():
    return render_template('student.html')

@app.route('/teacher-dashboard')
def teacher_dashboard():
    return render_template('teacher.html')

@app.route('/manager-dashboard')
def manager_dashboard():
    return render_template('manager.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)