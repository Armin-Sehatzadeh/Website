from flask import Flask, render_template
from database import db, TokenBlocklist
from flask_jwt_extended import JWTManager

from api.auth import auth_bp
from api.student import student_bp
from api.teacher import teacher_bp
from api.manager import manager_bp


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(student_bp, url_prefix="/api/student")
app.register_blueprint(teacher_bp, url_prefix="/api/teacher")
app.register_blueprint(manager_bp, url_prefix="/api/manager")

@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/login")
def login_page():
    return render_template("Login.html")

@app.route("/sign-in")
def sign_page():
    return render_template("Sign_in.html")


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.execute(
        db.select(TokenBlocklist).where(TokenBlocklist.jti == jti)
    ).scalar_one_or_none()

    return token is not None


if __name__ == "__main__":
    app.run(debug=True)
