# -*- coding: utf-8 -*-

from flask import Blueprint

chat = Blueprint('chat', __name__, template_folder='templates')

import flaskchat.chat.views
