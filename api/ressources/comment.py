from flask import Response, request
from api.models.Comment import Comment
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from .errors import SchemaValidationError, UserAlreadyExistsError, UserNotExistsError, DeletingUserError, \
    UpdatingUserError, InternalServerError
from ..models.user import User
from ..models.post import Post


class CommentsAPI(Resource):
    """
        TODO: Add admin ROLE to get all comments
        @jwt_required()
        def get(self):
            try:
                comments = Comment.objects().to_json()
                return Response(comments, mimetype="application/json", status=200)
            except DoesNotExist:
                raise UserNotExistsError
            except Exception:
                raise InternalServerError
    """

    @jwt_required()
    def post(self):
        try:
            post_id = request.args.get('post')
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            post = Post.objects.get(id=post_id)
            print(post.to_json())
            comment = Comment(**body, added_by=user, post_in=post).save()
            id = comment.id
            return {'id': str(id), "message": f'{comment.content} added successfully!'}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise UserAlreadyExistsError
        except Exception as e:
            raise InternalServerError

    @jwt_required()
    def get(self):
        try:
            post_id = request.args.get('post')
            comment = Comment.objects.get(post_in=post_id)
            return {'id': str(id), "message": f'{comment.content} added successfully!'}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise UserAlreadyExistsError
        except Exception as e:
            raise InternalServerError


class CommentAPI(Resource):
    @jwt_required()
    def get(self, id):
        try:
            users = User.objects.get(id=id).to_json()
            return Response(users, mimetype="application/json", status=200)
        except DoesNotExist:
            raise UserNotExistsError
        except Exception:
            raise InternalServerError
