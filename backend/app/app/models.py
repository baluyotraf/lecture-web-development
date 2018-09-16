from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()
ma = Marshmallow()


class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(60), nullable=False, unique=True)
    _password = Column('password', String(160), nullable=False)
    diary_entries = relationship('DiaryEntry', backref='user')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def check_password(self, given_password):
        return check_password_hash(self._password, given_password)


class DiaryEntry(db.Model):
    __tablename__ = 'diary_entry'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    body = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow())
    user_id = Column(Integer, ForeignKey('user.id'))


class UserSchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'username')


class DiaryEntrySchema(ma.ModelSchema):
    class Meta:
        fields = ('id', 'date', 'title', 'body')
