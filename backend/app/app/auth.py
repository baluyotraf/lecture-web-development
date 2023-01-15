from flask import current_app, request, jsonify
from functools import wraps
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from . models import User


_AUTHORIZATION_KEY = 'Authorization'
_FAILED_AUTH_MSG = {'message': 'Access Denied'}


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
    token_serializer = URLSafeTimedSerializer(secret_key)
    return token_serializer


def get_user_from_token(token):
    max_age = current_app.config['ITSDANGEROUS_EXPIRY_SECS']
    serializer = create_serializer()

    try:
        user_id = serializer.loads(token, max_age=max_age)['id']

    except (BadSignature, SignatureExpired, KeyError):
        return None

    return User.query.filter_by(id=user_id).first()


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
    return serializer.dumps({'id': user.id})


def requires_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_user()
        if user:
            return f(user, *args, **kwargs)
        else:
            return failed_auth_response()
    return decorated
