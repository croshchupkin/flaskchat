# -*- coding: utf-8 -*-

from flask import Blueprint

api = Blueprint('api', __name__, template_folder='templates')

import flaskchat.api.views
