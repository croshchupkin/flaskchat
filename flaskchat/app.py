# -*- coding: utf-8 -*-

from flask import Flask


def create_app(config_file_name):
    app = Flask('flaskchat', instance_relative_config=True)
    app.config.from_object('flaskchat.settings')
    app.config.from_pyfile(config_file_name)

    _init_db(app)
    _init_mail(app)
    _init_security(app)
    _init_blueprints(app)
    _init_context_processors(app)

    return app


def _init_db(app):
    from flaskchat.models import db
    db.init_app(app)


def _init_mail(app):
    from flaskchat.mail import mail
    mail.init_app(app)


def _init_security(app):
    from flaskchat.security import security, user_datastore
    from flaskchat.forms import ConfirmRegisterForm
    security.init_app(app, datastore=user_datastore,
                      confirm_register_form=ConfirmRegisterForm)


def _init_blueprints(app):
    from flaskchat.core import core
    app.register_blueprint(core)

    from flaskchat.chat import chat
    app.register_blueprint(chat, url_prefix='/chat')

    from flaskchat.api import api
    app.register_blueprint(api, url_prefix='/api')


def _init_context_processors(app):
    from flaskchat.forms import SearchChatForm

    @app.context_processor
    def add_chat_search_form():
        return {'chat_search_form': SearchChatForm()}
