# -*- coding: utf-8 -*-

from flask import current_app
from werkzeug.local import LocalProxy
from flask.ext.security import forms
from flask.ext.wtf import Form
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Length

from flaskchat.models import Chat


_datastore = LocalProxy(lambda: current_app.extensions['security'].datastore)


def unique_username(form, field):
    if _datastore.find_user(username=field.data) is not None:
        raise ValidationError('This username already exists')


def unique_chat_name(form, field):
    if Chat.query.filter_by(title=field.data).first() is not None:
        raise ValidationError('Chat with this title already exists')


class ConfirmRegisterForm(forms.ConfirmRegisterForm):
    username = StringField('Username', validators=[
        DataRequired('This field is required'),
        Length(min=1, max=255,
               message='Username must be between 1 and 255 characters long'),
        unique_username])


class CreateChatForm(Form):
    title = StringField('Title', validators=[
        DataRequired('This field is required'),
        Length(min=1, max=128,
               message='Chat title must be between 1 and 128 characters long'),
        unique_chat_name])


class SearchChatForm(Form):
    term = StringField('Search chat')
