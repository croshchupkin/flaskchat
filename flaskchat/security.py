# -*- coding: utf-8 -*-

from flask.ext.security import Security, SQLAlchemyUserDatastore

from flaskchat.models import db, User, Role
from flaskchat.forms import ConfirmRegisterForm

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore,
                    confirm_register_form=ConfirmRegisterForm)
