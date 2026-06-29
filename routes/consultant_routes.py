from flask import Blueprint, jsonify, request
from models.consultant import Consultant
from extensions import db
import requests

consultant_bp = Blueprint("consultant_bp", __name__)

# 🔥 GET ALL CONSULTANTS
@consultant_bp.route("/crm/consultants", methods=["GET"])
def get_consultants():
    consultants = Consultant.query.all()

    result = []
    for c in consultants:
        result.append({
            "id": str(c.id),
            "name": c.full_name,
            "mobile": c.phone,
            "city": c.city,
            "experience": f"{c.experience} yrs",
            "rating": 4.5,
            "totalConsultations": 0,
            "status": (c.status or "pending").lower(),

            "expertise": c.expertise.split(",") if c.expertise else [],
            "languages": c.languages.split(",") if c.languages else [],

            # ✅ ADD THIS
            "photo": c.photo,
            "certificate": c.certificate,
            "govt_id": c.govt_id,
        })

    return jsonify(result)


# 🔥 UPDATE STATUS (approve / deactivate)
@consultant_bp.route("/crm/update-consultant-status", methods=["POST"])
def update_status():

    data = request.json

    consultant = Consultant.query.get(data["id"])

    if not consultant:
        return {"status": "error"}

    consultant.status = data["status"]

    db.session.commit()

    # ✅ APPROVED
    if consultant.status.lower() == "approved":

        try:
            response = requests.post(
                "https://fundsarthi.onrender.com/api/send-notification",
                json={
                    "mobile": consultant.phone,
                    "title": "Consultant Application Approved",
                    "body": "Congratulations! Your Vastu Consultant application has been approved."
                },
                timeout=10
            )

            print("CONSULTANT APPROVAL PUSH:", response.text)

        except Exception as e:
            print("CONSULTANT PUSH ERROR:", str(e))

    # ❌ REJECTED
    elif consultant.status.lower() == "rejected":

        try:
            response = requests.post(
                "https://fundsarthi.onrender.com/api/send-notification",
                json={
                    "mobile": consultant.phone,
                    "title": "Consultant Application Rejected",
                    "body": "Your Vastu Consultant application could not be approved at this time."
                },
                timeout=10
            )

            print("CONSULTANT REJECT PUSH:", response.text)

        except Exception as e:
            print("CONSULTANT PUSH ERROR:", str(e))

    return {"status": "success"}


# 🔥 DELETE (reject)
@consultant_bp.route("/crm/delete-consultant/<id>", methods=["DELETE"])
def delete_consultant(id):
    consultant = Consultant.query.get(id)

    if not consultant:
        return {"status": "error"}

    db.session.delete(consultant)
    db.session.commit()

    return {"status": "success"}