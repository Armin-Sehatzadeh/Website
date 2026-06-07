from main import app
from database import db
from waitress import serve

print("Starting server...")

with app.app_context():
    db.create_all()

print("Server is running on http://127.0.0.1:5000")

serve(app, host="127.0.0.1", port=5000)
