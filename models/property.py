from extensions import db
from datetime import datetime

class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.String(20), unique=True)

    title = db.Column(db.String(255))
    property_type = db.Column(db.String(50))
    city = db.Column(db.String(100))
    locality = db.Column(db.String(255))

    price = db.Column(db.String(50))
    size = db.Column(db.String(50))

    bedrooms = db.Column(db.String(10))
    bathrooms = db.Column(db.String(10))

    description = db.Column(db.Text)

    name = db.Column(db.String(100))
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(100))

    # Property approval status
    status = db.Column(db.String(20), default="pending")

    # NEW FIELD
    listing_type = db.Column(
        db.String(50),
        default="normal"
    )

    photos = db.Column(db.Text)
    videos = db.Column(db.Text)
    floor_plans = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    purpose = db.Column(db.String(10))
    features = db.Column(db.Text)