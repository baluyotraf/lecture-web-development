from flask import current_app, request, jsonify
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired
from . models import User


_AUTHORIZATION_KEY = 'Authorization'
_FAILED_AUTH_MSG = {'message': 'Access Denied'}
_ENCODING = 'utf-8'


def failed_auth_response():
    return jsonify(_FAILED_AUTH_MSG), 401


def get_user_from_credentials(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    else:
        return None


def create_serializer():
    secret_key = current_app.config['ITSDANGEROUS_SECRET_KEY']
    token_serializer = TimedJSONWebSignatureSerializer(secret_key)
    return token_serializer


def get_user_from_token(token):
    try:
        serializer = create_serializer()
        user_id = serializer.loads(token)['id']
        user = User.query.filter_by(id=user_id).first()
        return user
    except (BadSignature, SignatureExpired, KeyError):
        return None


def get_user():
    auth = request.authorization
    if auth:
        return get_user_from_credentials(auth.username, auth.password)
    else:
        if _AUTHORIZATION_KEY in request.headers:
            _, token = request.headers[_AUTHORIZATION_KEY].split(None, 1)
            return get_user_from_token(token)
    return None


def generate_token(user):
    serializer = create_serializer()
    bytes_token = serializer.dumps({'id': user.id})
    return bytes_token.decode(_ENCODING)


def requires_user(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        user = get_user()
        if user:
            return func(user, *args, **kwargs)
        else:
            return failed_auth_response()
    return decorated
