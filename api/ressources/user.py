from flask import Response, request
from api.models.user import User
from flask_restful import Resource


class UsersApi(Resource):
    def get(self):
        users = User.objects().to_json()
        return Response(users, mimetype="application/json", status=200)

    def post(self):
        body = request.get_json()
        user = User(**body).save()
        id = user.id
        return {'id': str(id)}, 200


class UserApi(Resource):
    def put(self, id):
        body = request.get_json()
        User.objects.get(id=id).update(**body)
        return '', 200

    def delete(self, id):
        movie = User.objects.get(id=id).delete()
        return '', 200

    def get(self, id):
        movies = User.objects.get(id=id).to_json()
        return Response(movies, mimetype="application/json", status=200)
