from extensions import db
from datetime import datetime

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    booking_id = db.Column(db.String(20), unique=True)
    consultant_id = db.Column(db.Integer)

    consultant_name = db.Column(db.String(100))
    user_mobile = db.Column(db.String(15))
    customer_name = db.Column(db.String(100))

    consultation_type = db.Column(db.String(50))

    time = db.Column(db.Time)
    date = db.Column(db.Date)

    status = db.Column(db.String(20), default="scheduled")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)