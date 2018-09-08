from flask import Blueprint, jsonify, url_for


blueprint = Blueprint('index', __name__, url_prefix='/')


@blueprint.route('/')
def welcome():
    return 'welcome'

