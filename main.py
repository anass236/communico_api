from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager
from api.utils.database import initialize_db

from dotenv import load_dotenv
from os.path import dirname
from api.ressources.errors import errors
from flask_mail import Mail


dotenv_path = f'{dirname(__file__)}/.env'

load_dotenv(dotenv_path)

app = Flask(__name__)
app.config.from_object('api.config.default')
mail = Mail(app)
from api.ressources.routes import initialize_routes
api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


initialize_db(app)
initialize_routes(api)


