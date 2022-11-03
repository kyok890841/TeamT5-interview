from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from marshmallow import Schema, fields, pre_load, validate
from marshmallow import ValidationError

from flask import session
from .. import db

class TodoModel(db.Model):
    __tablename__ = 'todo'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    items = db.Column(db.String(60))
    expire_time = db.Column(db.DateTime)
    #update_time = db.Column(db.DateTime,
    #                        onupdate=datetime.now,
    #                        default=datetime.now)

    def __init__(self, todo_data, username):
        self.name = username
        self.items = todo_data['items']
        self.expire_time = todo_data['expire_time']

    @classmethod
    def get_todo_by_user(cls, name):
        print(name)
        return cls.query.filter_by(name=name).all()

    def save_db(self):
        db.session.add(self)
        db.session.commit()

    def save_session(self):
        session['username'] = self.name
        session['uid'] = self.uid
        session['items'] = self.items

    @staticmethod
    def remove_session():
        session['username'] = ''
        session['uid'] = ''

    @classmethod
    def update_db(cls, id, items, expire_time):
        print(id, items, expire_time)
        cls.query.filter_by(uid=id).update({'items':items, 'expire_time':expire_time})
        db.session.commit()
        
    @classmethod
    def delete_db(cls, id):
        cls.query.filter_by(uid=id).delete()
        db.session.commit()

    @classmethod
    def check_expired(cls):
        pass

class TodoSchema(Schema):
    uid = fields.Integer(dump_only=True)
    items = fields.String()
    expire_time = fields.DateTime(dt_format='iso8601')