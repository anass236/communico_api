import os

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
MONGODB_SETTINGS = dict(host=os.environ.get('DATABASE_URL'))
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_PORT = os.environ.get("MAIL_PORT")
MAIL_USER = os.environ.get("MAIL_USER")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
