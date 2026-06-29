from flask import Blueprint, request, jsonify
from models.admin import Admin
from extensions import db
import bcrypt

auth_bp = Blueprint("auth_bp", __name__)

# ✅ CREATE ADMIN
@auth_bp.route("/crm/create-admin", methods=["POST"])
def create_admin():
    try:
        data = request.json
        print("STEP 1")

        existing = Admin.query.filter_by(email=data.get("email")).first()
        print("STEP 2")

        if existing:
            return {"status": "error", "message": "Admin already exists"}

        hashed = bcrypt.hashpw(
            data.get("password").encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")
        print("STEP 3")

        admin = Admin(
            name=data.get("name"),
            email=data.get("email"),
            password=hashed
        )
        print("STEP 4")

        db.session.add(admin)
        print("STEP 5")

        db.session.commit()
        print("STEP 6")

        return {"status": "success", "message": "Admin created"}

    except Exception as e:
        print("CREATE ADMIN ERROR:", e)
        return {"error": str(e)}, 500
    

@auth_bp.route("/crm/test-admin", methods=["GET"])
def test_admin():
    try:
        count = Admin.query.count()
        return {
            "status": "success",
            "count": count
        }
    except Exception as e:
        print("TEST ADMIN ERROR:", e)
        return {
            "status": "error",
            "message": str(e)
        }, 500    


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