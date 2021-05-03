from flask import Flask
from api.utils.database import initialize_db
from flask_restful import Api
from api.ressources.routes import initialize_routes

app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/test_api'
}

initialize_db(app)
initialize_routes(api)

if __name__ == '__main__':
    app.run()
