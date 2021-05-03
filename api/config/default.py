import os

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
MONGODB_SETTINGS = dict(host=os.environ.get('DATABASE_URL'))