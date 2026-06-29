from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    
    city = db.Column(db.String(50))
    employment = db.Column(db.String(50))
    income = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 🔗 Relationship (optional but useful)
    loans = db.relationship("Loan", backref="user", lazy=True)