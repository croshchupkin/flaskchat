#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.script import Manager

from flaskchat.app import create_app
from flaskchat.models import db


manager = Manager(create_app('app.cfg'))


@manager.command
def create_db():
    db.create_all()


@manager.command
def drop_db():
    db.drop_all()


if __name__ == '__main__':
    manager.run()
