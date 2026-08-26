import os
from urllib.parse import quote_plus
import cloudinary

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

    DB_USER = os.getenv("DB_USER")
    DB_PASS = quote_plus(os.getenv("DB_PASS"))
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:3306/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }


# Reuses the same Cloudinary account as fundsarthi_backend (same env var
# names) so images uploaded from the CRM land in the same media library
# the app already reads from.
cloudinary.config(
    cloud_name=os.environ.get("CLOUD_NAME"),
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET")
)