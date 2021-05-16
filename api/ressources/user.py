from flask import Response, request
from api.models.user import User, Followers
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from .errors import SchemaValidationError, UserAlreadyExistsError, UserNotExistsError, DeletingUserError, \
    UpdatingUserError, InternalServerError

# Add Neo4j features
from ..utils.database import db_auth
from py2neo import Node, Relationship


class UsersApi(Resource):
    @jwt_required()
    def get(self):
        try:
            users = dict()
            users["users"] = []
            for user in User.objects():
                follow_list = [follow for follow in Followers.objects.filter(follower_username=user)]
                following_list = [follow for follow in Followers.objects.filter(added_by=user)]
                user = User.objects.get(id=user.id)
                user.update(followings=follow_list, followers=following_list)
                users["users"].append(user.to_json())
            return users, 200
        except DoesNotExist:
            raise UserNotExistsError
        except Exception:
            raise InternalServerError

    def post(self):
        try:
            body = request.get_json()
            user = User(**body).save()
            user_neo = Node("User", name=user.username, email=user.email)
            user_neo.__primarylabel__ = "User"
            user_neo.__primarykey__ = "name"
            db_auth.merge(user_neo)
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


class UserFollow(Resource):
    @jwt_required()
    def post(self):
        other_user_id = request.args.get('user')
        other_user = User.objects.get(id=other_user_id)
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        Followers(follower_username=other_user, added_by=user).save()
        follow_list = [follow for follow in Followers.objects.filter(added_by=user)]
        fans_list = [follow for follow in Followers.objects.filter(follower_username=user)]
        User.objects.get(id=user_id).update(followings=follow_list, followers=fans_list)
        return {'message': f'User {user_id} has followed {other_user_id}'}
