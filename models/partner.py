from extensions import db


class Partner(db.Model):
    __tablename__ = "partners"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    service_type = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    status = db.Column(
        db.Enum("pending", "approved", "rejected"),
        nullable=True,
        default="pending"
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "company": self.company,
            "service_type": self.service_type,
            "city": self.city,
            "phone": self.phone,
            "email": self.email,
            "status": self.status or "pending",
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
        }
