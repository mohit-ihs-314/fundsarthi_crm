from extensions import db


class PropertyEnquiry(db.Model):
    __tablename__ = "property_enquiries"

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, nullable=False)
    property_title = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    mobile = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(20),
        nullable=True,
        default="new"
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "property_id": self.property_id,
            "property_title": self.property_title or "",
            "name": self.name or "",
            "mobile": self.mobile or "",
            "email": self.email or "",
            "message": self.message or "",
            "status": (self.status or "new").lower(),
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
        }
