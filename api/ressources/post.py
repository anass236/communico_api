import io

from flask import send_file, request
from ..models.post import Post
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import ValidationError, InvalidQueryError, DoesNotExist, FieldDoesNotExist, NotUniqueError
from .errors import InternalServerError, SchemaValidationError, PostNotExistsError, PostAlreadyExistsError, \
    DeletingPostError, UpdatingPostError
from os.path import dirname
import os


class PostsApi(Resource):
    @jwt_required()
    def get(self, id):
        try:
            post = Post.objects.get(id=id)
            audio = post.audioPost.read()
            return send_file(io.BytesIO(audio), attachment_filename=post.title, mimetype='audio/mpeg')
        except DoesNotExist:
            raise PostNotExistsError
        except Exception:
            raise InternalServerError


class PostApi(Resource):
    @jwt_required()
    def post(self):
        try:
            body = request.get_json()
            post = Post(**body)
            os.rename(f'{dirname(__file__)}\\test.mp3', f'{dirname(__file__)}\\{post.audioFileName}')
            with open(f'{dirname(__file__)}\\{post.audioFileName}', 'rb') as fd:
                post.audioPost.put(fd, content_type='audio/mpeg')
            post.save()
            os.rename(f'{dirname(__file__)}\\{post.audioFileName}', f'{dirname(__file__)}\\test.mp3')
            return {'id': str(post.id), 'fileName': post.audioFileName}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except DoesNotExist:
            raise PostNotExistsError
        except NotUniqueError:
            raise PostAlreadyExistsError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def delete(self, id):
        try:
            posts = Post.objects.get(id=id).delete()
            return '', 200
        except DoesNotExist:
            raise DeletingPostError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def put(self, id):
        try:
            body = request.get_json()
            post = Post.objects.get(id=id).update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingPostError
        except DeletingPostError:
            raise InternalServerError
