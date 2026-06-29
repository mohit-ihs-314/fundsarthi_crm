import os
import cloudinary

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://u538772268_fund_user:B$S3=|3Gs9q^@srv2210.hstgr.io:3306/u538772268_fund_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


cloudinary.config(
    cloud_name="dsfsw8im3",
    api_key="124269824567964",
    api_secret="X5rcsWfPf0YYSdNqFTcjcMNiK9A"
)