import io

from flask import send_file, Response, request
from ..models.post import Post
from flask_restful import Resource
from os.path import dirname
import os


class PostsApi(Resource):
    def get(self, id):
        post = Post.objects.get(id=id)
        audio = post.audioPost.read()
        return send_file(io.BytesIO(audio), attachment_filename=post.title, mimetype='audio/mpeg')


class PostApi(Resource):
    def post(self):
        body = request.get_json()
        post = Post(**body)
        os.rename(f'{dirname(__file__)}\\test.mp3', f'{dirname(__file__)}\\{post.audioFileName}')
        with open(f'{dirname(__file__)}\\{post.audioFileName}', 'rb') as fd:
            post.audioPost.put(fd, content_type='audio/mpeg')
        post.save()
        os.rename(f'{dirname(__file__)}\\{post.audioFileName}', f'{dirname(__file__)}\\test.mp3')
        return {'id': str(post.id), 'fileName': post.audioFileName}, 200
