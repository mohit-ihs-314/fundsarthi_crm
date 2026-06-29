from flask import Blueprint, request, jsonify
from models.admin import Admin
from extensions import db
import bcrypt

auth_bp = Blueprint("auth_bp", __name__)

# ✅ CREATE ADMIN
@auth_bp.route("/crm/create-admin", methods=["POST"])
def create_admin():
    data = request.json

    existing = Admin.query.filter_by(email=data.get("email")).first()
    if existing:
        return {"status": "error", "message": "Admin already exists"}

    hashed = bcrypt.hashpw(
        data.get("password").encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    admin = Admin(
        name=data.get("name"),
        email=data.get("email"),
        password=hashed
    )

    db.session.add(admin)
    db.session.commit()

    return {"status": "success", "message": "Admin created"}


# ✅ LOGIN
@auth_bp.route("/crm/login", methods=["POST"])
def login():
    data = request.json

    admin = Admin.query.filter_by(email=data.get("email")).first()

    if not admin:
        return {"status": "error", "message": "Invalid credentials"}, 401

    try:
        if bcrypt.checkpw(
            data.get("password").encode("utf-8"),
            admin.password.encode("utf-8")   # ✅ ensure string → bytes
        ):
            return {
                "status": "success",
                "user": {
                    "id": admin.id,
                    "name": admin.name,
                    "email": admin.email
                }
            }
        else:
            return {"status": "error", "message": "Invalid credentials"}, 401

    except Exception as e:
        print("LOGIN ERROR:", e)
        return {"status": "error", "message": "Server error"}, 500