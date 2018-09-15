from importlib import import_module
from pkgutil import iter_modules
from flask import Flask
from .config import DefaultConfig
from .models import db, ma
from . import blueprints


def create_application(with_blueprints=True):
    application = Flask(__name__, static_folder=None)
    application.config.from_object(DefaultConfig())
    db.init_app(application)
    ma.init_app(application)
    if with_blueprints:
        register_blueprints(application)
    return application


def register_blueprints(application):
    modules = iter_modules(blueprints.__path__, blueprints.__name__ + '.')
    for _, m, _ in modules:
        module = import_module(m)
        application.register_blueprint(module.blueprint)
