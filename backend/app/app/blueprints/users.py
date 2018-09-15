from flask import Blueprint, jsonify, request, url_for
from ..models import db, User, UserSchema
from ..auth import requires_user, failed_auth_response


blueprint = Blueprint('users', __name__, url_prefix='/users')
schema = UserSchema()
_create_user_fields = ['username', 'password']


@blueprint.route('', methods=['POST'])
def create_users():
    user_details = request.get_json()
    user = User(**{field: user_details[field]
                   for field in _create_user_fields})
    db.session.add(user)
    db.session.commit()
    user_json = schema.dump(user).data
    return jsonify(user_json), 201, {'Location': url_for('.view_user', id_=user.id)}


@blueprint.route('/<int:id_>', methods=['GET'])
@requires_user
def view_user(user, id_):
    print('id:', id_)
    print('user:', user)
    if user.id == id_:
        user_json = schema.dump(user).data
        return jsonify(user_json), 200
    else:
        return failed_auth_response()

