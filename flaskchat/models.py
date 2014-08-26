# -*- coding: utf-8 -*-

import datetime
import calendar

from flask import json
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import RoleMixin, UserMixin

db = SQLAlchemy()

roles_users = db.Table('roles_users',
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('roles.id'), primary_key=True),
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('users.id'), primary_key=True))


users_chat_subscriptions = db.Table('users_chat_subscriptions',
                                    db.Column('user_id', db.Integer(),
                                              db.ForeignKey('users.id'),
                                              primary_key=True),
                                    db.Column('chat_id', db.Integer(),
                                              db.ForeignKey('chats.id'),
                                              primary_key=True))


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class Chat(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(128), unique=True)

    def __repr__(self):
        return '<Chat {}>'.format(self.title)


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), index=True,
                           default=datetime.datetime.utcnow)
    chat_id = db.Column(db.Integer(), db.ForeignKey('chats.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    chat = db.relationship('Chat', backref=db.backref('messages',
                                                      lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('chat_messages',
                                                      lazy='dynamic'))

    def __repr__(self):
        return '<ChatMessage from {}>'.format(self.user.username)

    def to_dict(self):
        return {
            'id': self.id,
            'created_at': calendar.timegm(self.created_at.timetuple()) * 1000,
            'author': self.user.username,
            'text': self.text
        }


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    chat_subscriptions = db.relationship(
        'Chat',
        secondary=users_chat_subscriptions,
        backref='subscribed_users')

    def is_subscribed_to_chat(self, chat):
        return chat in self.chat_subscriptions

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def to_dict(self):
        return {
            'username': self.username
        }

    def to_json(self):
        return json.dumps(self.to_dict())
