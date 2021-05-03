from .user import UserApi, UsersApi
from .auth import SignupApi, LoginApi
from .post import PostsApi, PostApi


def initialize_routes(api):
    api.add_resource(UsersApi, '/api/users')
    api.add_resource(UserApi, '/api/user/<id>')
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    # Posts
    api.add_resource(PostApi, '/api/post')
    api.add_resource(PostsApi, '/api/posts/<id>')
