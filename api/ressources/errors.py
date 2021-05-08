class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


'''
    User Exceptions
'''


class UserAlreadyExistsError(Exception):
    pass


class UpdatingUserError(Exception):
    pass


class DeletingUserError(Exception):
    pass


class UserNotExistsError(Exception):
    pass


'''
    Posts Exceptions
'''


class PostAlreadyExistsError(Exception):
    pass


class UpdatingPostError(Exception):
    pass


class DeletingPostError(Exception):
    pass


class PostNotExistsError(Exception):
    pass


'''
    Comments Exceptions
'''


class DeletingCommentError(Exception):
    pass


class CommentNotExistsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class EmailDoesNotExistsError(Exception):
    pass


class BadTokenError(Exception):
    pass


class ExpiredTokenError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "UserAlreadyExistsError": {
        "message": "User with given username already exists",
        "status": 400
    },
    "UpdatingUserError": {
        "message": "Updating user added by other is forbidden",
        "status": 403
    },
    "DeletingUserError": {
        "message": "Deleting User added by other is forbidden",
        "status": 403
    },
    "UserNotExistsError": {
        "message": "User with given id doesn't exists",
        "status": 400
    },
    "PostAlreadyExistsError": {
        "message": "Post with given title already exists",
        "status": 400
    },
    "UpdatingPostError": {
        "message": "Updating post added by other is forbidden",
        "status": 403
    },
    "DeletingPostError": {
        "message": "Deleting Post added by other is forbidden",
        "status": 403
    },
    "PostNotExistsError": {
        "message": "Post with given id doesn't exists",
        "status": 400
    },
    "DeletingCommentError": {
        "message": "Deleting Comment added by other is forbidden",
        "status": 403
    },
    "CommentNotExistsError": {
        "message": "Comment with given id doesn't exists",
        "status": 400
    },
    "EmailAlreadyExistsError": {
        "message": "User with given email address already exists",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    },
    "EmailDoesNotExistsError": {
        "message": "Couldn't find the user with given email address",
        "status": 403
    },
    "BadTokenError": {
        "message": "Invalid Token used",
        "status": 401
    },
    "ExpiredTokenError": {
        "message": "Your token is expired try to login again !!",
        "status": 401
    }
}
