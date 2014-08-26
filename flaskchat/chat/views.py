# -*- coding: utf-8 -*-

from flask import (render_template, redirect, url_for, request, current_app,
                   abort, json)
from flask.ext.security.decorators import login_required
from flask.ext.security.core import current_user

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
        c.subscribed_users.append(current_user)
        db.session.add(c)
        db.session.commit()

        return redirect(url_for('chat.show', chat_id=c.id))

    return render_template('chat/create.html', form=form)


@chat.route('/search')
@chat.route('/search/<int:page>')
@login_required
def search(page=1):
    term = request.args.get('term', '')
    page = page if page > 0 else 1
    per_page = current_app.config['CHAT_SEARCH_PER_PAGE']

    pagination = (Chat.query
                  .filter(Chat.title.ilike(u'%{}%'.format(term)))
                  .order_by('title')
                  .paginate(page, per_page))

    return render_template('chat/search.html', term=term,
                           pagination=pagination)


@chat.route('/list')
@chat.route('/list/<int:page>')
@login_required
def list(page=1):
    page = page if page > 0 else 1
    per_page = current_app.config['CHAT_LIST_PER_PAGE']
    pagination = Chat.query.order_by('title').paginate(page, per_page)

    return render_template('chat/list.html', pagination=pagination)


@chat.route('/subscribe/<int:chat_id>', methods=['POST'])
@login_required
def subscribe(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if not current_user.is_subscribed_to_chat(chat):
        current_user.chat_subscriptions.append(chat)
        db.session.commit()

    return redirect(url_for('chat.show', chat_id=chat_id))


@chat.route('/unsubscribe/<int:chat_id>', methods=['POST'])
@login_required
def unsubscribe(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if current_user.is_subscribed_to_chat(chat):
        current_user.chat_subscriptions.remove(chat)
        db.session.commit()

    return redirect(url_for('core.index'))


@chat.route('/show/<int:chat_id>')
@login_required
def show(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    if not current_user.is_subscribed_to_chat(chat):
        abort(404)

    users_json = json.dumps([u.to_dict() for u in chat.subscribed_users])
    messages_json = json.dumps([m.to_dict() for m in chat.messages.all()])

    return render_template('chat/show.html', active_chat=chat,
                           initial_users_json=users_json,
                           initial_messages_json=messages_json)
