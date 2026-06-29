from flask import Blueprint, jsonify, request
from models.loan import Loan, LoanStep
from models.user import User
from extensions import db
import json
import requests

loan_bp = Blueprint("loan_bp", __name__)
user_bp = Blueprint("user_bp", __name__)

def parse_loan_amount(amount):
    if not amount:
        return 0

    amount = str(amount).strip().upper()

    try:
        if amount.endswith("L"):
            return int(float(amount[:-1]) * 100000)

        if amount.endswith("CR"):
            return int(float(amount[:-2]) * 10000000)

        return int(float(amount))

    except Exception:
        return 0

@loan_bp.route("/crm/loans", methods=["GET"])
def get_loans():
    loans = Loan.query.all()
    result = []

    for loan in loans:
        user = User.query.get(loan.user_id)

        # 🔥 SAFE JSON PARSE
        if isinstance(loan.extra_data, str):
            form_data = json.loads(loan.extra_data)
        elif isinstance(loan.extra_data, dict):
            form_data = loan.extra_data
        else:
            form_data = {}

        # steps
        steps = LoanStep.query.filter_by(loan_id=loan.id).all()
        completed_steps = sum(1 for s in steps if s.is_done)

        current_step = completed_steps + 1 if completed_steps < 4 else 4
        progress = int((completed_steps / 4) * 100)

        result.append({
            "id": loan.application_id,
            "userName": user.name if user else (loan.customer_name or ""),
            "email": "",
            "mobile": user.mobile if user else (loan.mobile or ""),
            "loanAmount": parse_loan_amount(loan.loan_amount),
            "loanType": loan.loan_type or "",
            "status": (loan.status or "").lower(),
            "currentStep": current_step,
            "progress": progress,
            "isRejected": (loan.status or "").lower() == "rejected",
            "notes": loan.notes or "",
            "appliedDate": "N/A",
            "city": user.city if user else "",
            "employment": user.employment if user else "",
            "income": user.income if user else 0,
            "formData": form_data  # ✅ FIXED
        })

    return jsonify(result)

@loan_bp.route("/crm/update-status", methods=["POST"])
def update_status():
    data = request.json

    loan = Loan.query.filter_by(application_id=data["loanId"]).first()

    if not loan:
        return {"status": "error", "message": "Loan not found"}

    # 🔴 REJECT CASE
    if data.get("status") == "rejected":
        loan.status = "Rejected"

        # sab steps stop
        steps = LoanStep.query.filter_by(loan_id=loan.id).all()
        for step in steps:
            if step.is_done:
                continue
            step.is_done = False

        db.session.commit()

        user = User.query.get(loan.user_id)

        if user:

            try:

                response = requests.post(
                    "https://fundsarthi.onrender.com/api/send-notification",
                    json={
                        "mobile": user.mobile,
                        "title": "Loan Application Update",
                        "body": "Unfortunately your loan application was rejected."
                    },
                    timeout=10
                )

                print("NOTIFICATION RESPONSE:", response.text)

            except Exception as e:

                print("NOTIFICATION ERROR:", str(e))

        return {"status": "success"}

    # 🟢 NORMAL FLOW (STEP UPDATE)
    next_step = data.get("currentStep")

    steps = LoanStep.query.filter_by(loan_id=loan.id).order_by(LoanStep.id).all()

    for index, step in enumerate(steps, start=1):
        if index < next_step:
            step.is_done = True
        elif index >= next_step:
            step.is_done = False

    # status update logic
    if next_step == 1:
        loan.status = "New"
    elif next_step in [2, 3]:
        loan.status = "In-Process"
    elif next_step == 4:
        loan.status = "Approved"

    db.session.commit()

    # 🔥 SEND PUSH NOTIFICATION
    user = User.query.get(loan.user_id)

    print("LOAN USER:", user)

    if user:

        try:

            response = requests.post(
                "https://fundsarthi.onrender.com/api/send-notification",
                json={
                    "mobile": user.mobile,
                    "title": "Loan Status Updated",
                    "body": f"Your loan status is now {loan.status}"
                },
                timeout=10
            )

            print("NOTIFICATION RESPONSE:", response.text)

        except Exception as e:

            print("NOTIFICATION ERROR:", str(e))

    return {"status": "success"}

@loan_bp.route("/loan/<application_id>", methods=["GET"])
def get_single_loan(application_id):
    loan = Loan.query.filter_by(application_id=application_id).first()

    if not loan:
        return {"status": "error"}

    user = User.query.get(loan.user_id)

    steps = LoanStep.query.filter_by(loan.id).all()

    return jsonify({
        "loan": loan.application_id,
        "user": user.name if user else "",
        "steps": [
            {
                "name": s.step_name,
                "done": s.is_done
            } for s in steps
        ]
    })

@user_bp.route("/crm/users", methods=["GET"])
def get_users():
    users = User.query.all()

    print("🔥 USERS FETCHED:", users)   # debug

    result = []
    for u in users:
        result.append({
            "id": u.id,
            "name": u.name,
            "email": getattr(u, "email", ""),  # 🔥 SAFE
            "mobile": u.mobile,
            "city": u.city,
            "employment": u.employment,
            "income": u.income,
            "totalLoans": len(u.loans),
            "approvedLoans": len([l for l in u.loans if l.status == "Approved"])
        })

    return jsonify(result)