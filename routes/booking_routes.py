from flask import Blueprint, jsonify, request
from models.booking import Booking
from extensions import db

booking_bp = Blueprint("booking_bp", __name__)

@booking_bp.route("/crm/bookings", methods=["GET"])
def get_bookings():
    bookings = Booking.query.all()

    result = []
    for b in bookings:
        result.append({
            "id": b.booking_id,
            "consultantName": b.consultant_name or "",
            "customerName": b.customer_name or "",
            "customerMobile": b.user_mobile or "",
            "time": b.time.strftime("%H:%M") if b.time else "",
            "date": b.date.strftime("%Y-%m-%d") if b.date else "",
            "status": (b.status or "scheduled").lower(),
            
        })

    return jsonify(result)

@booking_bp.route("/crm/update-booking-status", methods=["POST"])
def update_booking_status():
    data = request.json

    booking = Booking.query.filter_by(booking_id=data["id"]).first()

    if not booking:
        return {"status": "error", "message": "Booking not found"}

    booking.status = data.get("status", "completed")

    db.session.commit()

    return {"status": "success"}