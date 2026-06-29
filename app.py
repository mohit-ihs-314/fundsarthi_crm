from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db
from routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Enable CORS (Frontend access)
    CORS(app)

    # ✅ Init Database
    db.init_app(app)

    app.register_blueprint(auth_bp)

    # ✅ Import routes
    from routes.loan_routes import loan_bp, user_bp
    from routes.consultant_routes import consultant_bp
    from routes.booking_routes import booking_bp
    from routes.property_routes import property_bp

    # ✅ Register routes
    app.register_blueprint(loan_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(consultant_bp, url_prefix="/api")
    app.register_blueprint(booking_bp, url_prefix="/api")
    app.register_blueprint(property_bp, url_prefix="/api")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5001)