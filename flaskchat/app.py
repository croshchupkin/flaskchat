# -*- coding: utf-8 -*-

from flask import Flask, request


def create_app(config_file_name):
    app = Flask('flaskchat', instance_relative_config=True)
    app.config.from_object('flaskchat.settings')
    app.config.from_pyfile(config_file_name)

    _init_db(app)
    _init_mail(app)
    _init_security(app)

    return app


def _init_db(app):
    from flaskchat.models import db
    db.init_app(app)


def _init_mail(app):
    from flaskchat.mail import mail
    mail.init_app(app)


def _init_security(app):
    from flaskchat.security import security
    security.init_app(app)
