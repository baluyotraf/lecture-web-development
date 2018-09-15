from flask_env import MetaFlaskEnv


class DefaultConfig(metaclass=MetaFlaskEnv):
    SQLALCHEMY_DATABASE_URI = 'mysql://user:user@database/db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITSDANGEROUS_SECRET_KEY = 'hello'
    ITSDANGEROUS_EXPIRY_SECS = 24 * 3600
