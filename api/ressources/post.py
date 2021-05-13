from flask import request, Response

from ..models.Comment import Comment
from ..models.post import Post
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from mongoengine.errors import ValidationError, InvalidQueryError, DoesNotExist, FieldDoesNotExist, NotUniqueError
from .errors import InternalServerError, SchemaValidationError, PostNotExistsError, PostAlreadyExistsError, \
    DeletingPostError, UpdatingPostError
from ..models.user import User


class PostsApi(Resource):
    @jwt_required()
    def get(self, id):
        try:
            comments = [com for com in Comment.objects.filter(post_in=id)]
            post = Post.objects.get(id=id)
            user_id = get_jwt_identity()
            user = User.objects.get(id=user_id)
            posts = [post for post in Post.objects.filter(added_by=user)]
            user.update(posts=posts)
            post.update(comments=comments)
            return Response(post.to_result(), mimetype="application/json", status=200)
            # audio = post.audioPost.read()
            # return send_file(io.BytesIO(audio), attachment_filename=post.title, mimetype='audio/mpeg')
        except DoesNotExist:
            raise PostNotExistsError
        except Exception:
            raise InternalServerError


class PostApi(Resource):
    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            post = Post(**body, added_by=user).save()
            posts = [post for post in Post.objects.filter(added_by=user)]
            user.update(posts=posts)
            return {'id': str(post.id)}, 200
            # os.rename(f'{dirname(__file__)}\\test.mp3', f'{dirname(__file__)}\\{post.audioFileName}')
            # with open(f'{dirname(__file__)}\\{post.audioFileName}', 'rb') as fd:
            #    post.audioPost.put(fd, content_type='audio/mpeg')
            # post.save()
            # os.rename(f'{dirname(__file__)}\\{post.audioFileName}', f'{dirname(__file__)}\\test.mp3')
            # return {'id': str(post.id), 'fileName': post.audioFileName}, 200
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
            return {'message': f'Delete of Post #{posts.id} is successful!'}, 200
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
