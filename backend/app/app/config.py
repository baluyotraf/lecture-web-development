from flask_env import MetaFlaskEnv


class DefaultConfig(metaclass=MetaFlaskEnv):
    SQLALCHEMY_DATABASE_URI = 'mysql://user:user@database/db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
