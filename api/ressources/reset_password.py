from flask import request, render_template
from flask_jwt_extended import create_access_token, decode_token
from ..models.user import User
from flask_restful import Resource
import datetime
from .errors import SchemaValidationError, InternalServerError, EmailDoesNotExistsError, BadTokenError, ExpiredTokenError
from jwt.exceptions import ExpiredSignatureError, DecodeError, InvalidTokenError
from ..services.mailservice import send_email


class ForgotPassword(Resource):
    def post(self):
        url = request.host_url + 'reset/'
        try:
            body = request.get_json()
            email = body.get('email')
            print(f'email: {email}')
            if not email:
                raise SchemaValidationError

            user = User.objects.get(email=email)
            print(f'email: {user}')
            if not User:
                raise EmailDoesNotExistsError

            expires = datetime.timedelta(hours=24)
            reset_token = create_access_token(str(user.id), expires_delta=expires)
            return send_email('[communico] Reset Your password',
                              sender='support@communico.com',
                              recipients=[user.email],
                              text_body=render_template('email/reset_password.txt',
                                                        url=url + reset_token),
                              html_body=render_template('email/reset_password.html',
                                                        url=url + reset_token))
        except SchemaValidationError:
            raise SchemaValidationError
        except EmailDoesNotExistsError:
            raise EmailDoesNotExistsError
        except Exception:
            raise InternalServerError


class ResetPassword(Resource):
    def post(self):
        try:
            body = request.get_json()
            reset_token = body.get('reset_token')
            password = body.get('password')

            if not reset_token or not password:
                raise SchemaValidationError

            user_id = decode_token(reset_token)['sub']

            user = User.objects.get(id=user_id)

            user.modify(password=password)
            user.hash_password()
            user.save()

            return send_email('[Communico] Password reset successful',
                              sender='support@communico.com',
                              recipients=[user.email],
                              text_body='Password reset was successful',
                              html_body='<p>Password reset was successful</p>')

        except SchemaValidationError:
            raise SchemaValidationError

        except ExpiredSignatureError:
            raise ExpiredTokenError

        except (DecodeError, InvalidTokenError):
            raise BadTokenError
        except Exception as e:
            raise InternalServerError
