from .comment import CommentAPI, CommentsAPI
from .user import UserApi, UsersApi, UserFollow
from .auth import SignupApi, LoginApi
from .post import PostsApi, PostApi
from .reset_password import ForgotPassword, ResetPassword


def initialize_routes(api):
    api.add_resource(UsersApi, '/api/users')
    api.add_resource(UserApi, '/api/user/<id>')
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
    # Posts
    api.add_resource(PostApi, '/api/post')
    api.add_resource(PostsApi, '/api/posts/<id>')
    # Password reset
    api.add_resource(ForgotPassword, '/api/auth/forgot')
    api.add_resource(ResetPassword, '/api/auth/reset')
    # Comments
    api.add_resource(CommentAPI, '/api/comment/<id>')
    api.add_resource(CommentsAPI, '/api/comment')
    # Follow
    api.add_resource(UserFollow, '/api/user/follow')
