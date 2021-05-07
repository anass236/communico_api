import datetime
from flask import request
from flask_jwt_extended import create_access_token
from api.models.user import User
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, ValidationError, DoesNotExist, NotUniqueError
from .errors import InternalServerError, EmailAlreadyExistsError, SchemaValidationError, UnauthorizedError


class SignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User(**body)
            user.hash_password()
            user.save()
            id = user.id
            return {'id': str(id), 'message': 'Signup is successful'}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception:
            raise InternalServerError


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                raise UnauthorizedError

            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'token': access_token, 'message': f'{user.username} is authenticated'}, 200
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception:
            raise InternalServerError
