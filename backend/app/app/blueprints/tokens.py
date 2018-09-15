from flask import Blueprint, jsonify
from ..auth import requires_user, generate_token


blueprint = Blueprint('tokens', __name__, url_prefix='/tokens')


@blueprint.route('/', methods=['GET'])
@requires_user
def get_token(user):
    response = {
        'tokens': generate_token(user)
    }
    return jsonify(response), 200
