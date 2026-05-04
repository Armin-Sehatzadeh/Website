from flask import Flask, render_template
from database import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    
    
@app.route("/")
def home():
    return render_template("Home.html")

@app.route("/login")
def login_page():
    return render_template("Login.html")

@app.route("/sign-in")
def sign_page():
    return render_template("Sign_in.html")



if __name__ == "__main__":
    app.run(debug=True)
