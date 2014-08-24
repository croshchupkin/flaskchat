# -*- coding: utf-8 -*-

from flask import render_template

from flaskchat.core import core


@core.route('/')
def index():
    return render_template('index.html')
