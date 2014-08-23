# -*- coding: utf-8 -*-

import datetime

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import RoleMixin, UserMixin

db = SQLAlchemy()

roles_users = db.Table('roles_users',
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('roles.id')),
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('users.id')))


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return '<Chat {}>'.format(self.title)


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.BigInteger(), primary_key=True)
    text = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), index=True,
                           default=datetime.datetime.utcnow)
    chat_id = db.Column(db.Integer(), db.ForeignKey('chats.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    chat = db.relationship('Chat', backref=db.backref('messages',
                                                      lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('chat_messages',
                                                      lazy='dynamic'))
