# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for
from flask.ext.security.decorators import login_required

from flaskchat.chat import chat
from flaskchat.forms import CreateChatForm
from flaskchat.models import db, Chat


@chat.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateChatForm()

    if form.validate_on_submit():
        c = Chat()
        c.title = form.title.data
        db.session.add(c)
        db.session.commit()

        return redirect(url_for('core.index'))

    return render_template('chat/create.html', form=form)
