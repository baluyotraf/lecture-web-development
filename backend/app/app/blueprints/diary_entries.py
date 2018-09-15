from flask import Blueprint, jsonify, request, url_for
from ..models import db, DiaryEntry, DiaryEntrySchema
from ..auth import requires_user, failed_auth_response
from functools import wraps


blueprint = Blueprint('diary_entries', __name__, url_prefix='/diary_entries')
schema = DiaryEntrySchema()
_diary_entry_fields = ['title', 'body']


def _jsonify_diary(model):
    diary_dict = schema.dump(model).data
    return jsonify(diary_dict)


def requires_diary_entry(f):
    @wraps(f)
    def decorated(user, id_, *args, **kwargs):
        diary_entry = DiaryEntry.query.get_or_404(id_)
        if diary_entry.user_id != user.id:
            return failed_auth_response()
        else:
            return f(diary_entry, *args, **kwargs)
        pass
    return decorated


@blueprint.route('', methods=['POST'])
@requires_user
def create_diary_entry(user):
    diary_entry_inputs = request.get_json()
    diary_entry = DiaryEntry(user_id=user.id,
                             **{field: diary_entry_inputs[field]
                                for field in _diary_entry_fields})
    db.session.add(diary_entry)
    db.session.commit()
    location = url_for('.view_diary_entry', id_=diary_entry.id)
    return _jsonify_diary(diary_entry), 201, {'Location': location}


@blueprint.route('/<int:id_>', methods=['GET'])
@requires_user
@requires_diary_entry
def view_diary_entry(diary_entry):
    return _jsonify_diary(diary_entry), 200


@blueprint.route('/<int:id_>', methods=['PATCH'])
@requires_user
@requires_diary_entry
def edit_diary_entry(diary_entry):
    diary_entry_inputs = request.get_json()
    for field in _diary_entry_fields:
        try:
            value = diary_entry_inputs[field]
        except KeyError:
            continue
        setattr(diary_entry, field, value)
    db.session.commit()
    return _jsonify_diary(diary_entry), 200


@blueprint.route('/<int:id_>', methods=['DELETE'])
@requires_user
@requires_diary_entry
def delete_diary_entry(diary_entry):
    db.session.delete(diary_entry)
    db.session.commit()
    return jsonify({}), 204




