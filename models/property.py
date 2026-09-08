from extensions import db
from datetime import datetime


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)

    property_id = db.Column(
        db.String(20),
        unique=True
    )

    title = db.Column(db.String(255))

    property_type = db.Column(
        db.String(50)
    )

    city = db.Column(
        db.String(100)
    )

    locality = db.Column(
        db.String(255)
    )

    latitude = db.Column(
        db.Float
    )

    longitude = db.Column(
        db.Float
    )

    price = db.Column(
        db.String(50)
    )

    size = db.Column(
        db.String(50)
    )

    bedrooms = db.Column(
        db.String(10)
    )

    bathrooms = db.Column(
        db.String(10)
    )

    description = db.Column(
        db.Text
    )

    name = db.Column(
        db.String(100)
    )

    mobile = db.Column(
        db.String(20)
    )

    email = db.Column(
        db.String(100)
    )

    # -----------------------------------
    # PROPERTY APPROVAL STATUS
    # -----------------------------------

    status = db.Column(
        db.String(20),
        default="pending"
    )

    # -----------------------------------
    # LISTING TYPE
    # -----------------------------------

    listing_type = db.Column(
        db.String(50),
        default="normal"
    )

    # -----------------------------------
    # MANUAL PROMOTION FLAGS
    # -----------------------------------

    # 0 = normal
    # 1 = Hot Deal
    is_hot_deal = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    # 0 = normal
    # 1 = Trending
    is_trending = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    # Lower number = higher position
    hot_deal_order = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    trending_order = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    # -----------------------------------
    # MEDIA
    # -----------------------------------

    photos = db.Column(
        db.Text
    )

    videos = db.Column(
        db.Text
    )

    floor_plans = db.Column(
        db.Text
    )

    # -----------------------------------
    # CREATED DATE
    # -----------------------------------

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # -----------------------------------
    # PURPOSE
    # -----------------------------------

    purpose = db.Column(
        db.String(10)
    )

    # -----------------------------------
    # FEATURES
    # -----------------------------------

    features = db.Column(
        db.Text
    )