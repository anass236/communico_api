import os

from flask_mongoengine import MongoEngine
from py2neo import Graph
from dotenv import load_dotenv

dotenv_path = f'C:/Users/anass/PycharmProjects/communico_api/.env'
load_dotenv(dotenv_path)
db = MongoEngine()
print(os.environ["NEO4J_HOST"])

db_auth = Graph(os.environ["NEO4J_HOST"], auth=(os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"]))


def initialize_db(app):
    db.init_app(app)
