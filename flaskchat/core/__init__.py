# -*- coding: utf-8 -*-

from flask import Blueprint

core = Blueprint('core', __name__, template_folder='templates')

import flaskchat.core.views
