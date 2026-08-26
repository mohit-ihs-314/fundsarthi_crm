from extensions import db

class AppSettings(db.Model):
    __tablename__ = "app_settings"

    id = db.Column(db.Integer, primary_key=True)

    nearby_radius_km = db.Column(db.Float, default=2)

    budget_deal_max = db.Column(db.Float, default=20000000)
    luxury_min = db.Column(db.Float, default=20000000)
    luxury_max = db.Column(db.Float, default=30000000)
    premium_min = db.Column(db.Float, default=100000000)

    recommended_salary_multiplier = db.Column(db.Float, default=10)


DEFAULT_SETTINGS = {
    "nearby_radius_km": 2,
    "budget_deal_max": 20000000,
    "luxury_min": 20000000,
    "luxury_max": 30000000,
    "premium_min": 100000000,
    "recommended_salary_multiplier": 10,
}


def get_settings():
    settings = AppSettings.query.get(1)

    if not settings:
        settings = AppSettings(id=1, **DEFAULT_SETTINGS)
        db.session.add(settings)
        db.session.commit()

    return settings
