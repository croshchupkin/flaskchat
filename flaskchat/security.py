# -*- coding: utf-8 -*-

from flask.ext.security import Security, SQLAlchemyUserDatastore

from flaskchat.models import db, User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)
