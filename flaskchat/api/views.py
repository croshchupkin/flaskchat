# -*- coding: utf-8 -*-

from datetime import datetime

from flask import request, abort, current_app, jsonify
from werkzeug.local import LocalProxy
from flask.ext.security.decorators import login_required

from flaskchat.api import api
from flaskchat.models import db, Chat, ChatMessage

_datastore = LocalProxy(lambda: current_app.extensions['security'].datastore)


@api.route('/chat/<int:chat_id>/messages', methods=['POST'])
@login_required
def save_message(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    json = request.get_json()
    username = json.get('author')
    text = json.get('text')
    created_at = json.get('created_at')

    if not all([username, text, created_at]):
        abort(400)

    user = _datastore.find_user(username=username)
    if not user:
        abort(400)

    message = ChatMessage()
    message.user = user
    message.chat = chat
    message.text = text
    message.created_at = datetime.utcfromtimestamp(created_at // 1000)

    db.session.add(message)
    db.session.commit()

    return ''


@api.route('/chat/<int:chat_id>/messages', methods=['GET'])
@login_required
def get_messages(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    messages = [m.to_dict() for m in chat.messages.all()]
    return jsonify(result=messages)


@api.route('/chat/<int:chat_id>/users', methods=['GET'])
def get_users(chat_id):
    chat = Chat.query.get_or_404(chat_id)
    users = [u.to_dict() for u in chat.subscribed_users]
    return jsonify(result=users)
