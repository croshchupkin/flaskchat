# -*- coding: utf-8 -*-

from flask import current_app
from werkzeug.local import LocalProxy
from flask.ext.security import forms
from wtforms import StringField, ValidationError
from wtforms.validators import DataRequired, Length

_datastore = LocalProxy(lambda: current_app.extensions['security'].datastore)


def unique_username(form, field):
    if _datastore.find_user(username=field.data) is not None:
        raise ValidationError('This username already exists')


class ConfirmRegisterForm(forms.ConfirmRegisterForm):
    username = StringField('Username', validators=[
        DataRequired('This field is required'),
        Length(min=1, max=255,
               message='Username must be between 1 and 255 characters'),
        unique_username])
