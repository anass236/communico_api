from flask import Response, request
from api.models.user import User
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from .errors import SchemaValidationError, UserAlreadyExistsError, UserNotExistsError, DeletingUserError, \
    UpdatingUserError, InternalServerError


class UsersApi(Resource):
    @jwt_required()
    def get(self):
        try:
            users = User.objects().to_json()
            return Response(users, mimetype="application/json", status=200)
        except DoesNotExist:
            raise UserNotExistsError
        except Exception:
            raise InternalServerError

    def post(self):
        try:
            body = request.get_json()
            user = User(**body).save()
            id = user.id
            return {'id': str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise UserAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class UserApi(Resource):
    @jwt_required()
    def put(self, id):
        try:
            body = request.get_json()
            User.objects.get(id=id).update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingUserError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def delete(self, id):
        try:
            user = User.objects.get(id=id).delete()
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise DeletingUserError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def get(self, id):
        try:
            users = User.objects.get(id=id).to_json()
            return Response(users, mimetype="application/json", status=200)
        except DoesNotExist:
            raise UserNotExistsError
        except Exception:
            raise InternalServerError
