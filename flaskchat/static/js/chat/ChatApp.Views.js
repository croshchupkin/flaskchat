'use strict';

ChatApp.module('Views', function(Views, App, Backbone, Marionette, $, _) {
    Views.ChatMessage = Marionette.ItemView.extend({
        template: '#tpl-chat-message-view',

        templateHelpers: {
            'formattedDate': function() {
                return moment(this.created_at).format('YYYY-MM-DD HH:mm');
            }
        }
    });

    Views.ChatMessageList = Marionette.CompositeView.extend({
        template: '#tpl-chat-message-list',
        childView: Views.ChatMessage,
        childViewContainer: '#chat-messages-container',

        initialize: function() {
            var self = this;
            ChatApp.on('messageInput:newMessage', function(message) {
                self.collection.create(message);
            });
        },

        onShow: function() {
            this.scrollToBottom();
            this.startSyncing();
        },

        onAddChild: function() {
            this.scrollToBottom();
        },

        scrollToBottom: function() {
            var container = this.$('#chat-messages-container').get(0);
            container.scrollTop = container.scrollHeight;
        },

        startSyncing: function() {
            window.setInterval(_.bind(this.syncMessages, this), 1000);
        },

        syncMessages: function() {
            this.collection.fetch();
        }
    });

    Views.User = Marionette.ItemView.extend({
        template: '#tpl-user-view'
    });

    Views.UserList = Marionette.CollectionView.extend({
        childView: Views.User,

        onShow: function() {
            this.startSyncing();
        },

        startSyncing: function() {
            window.setInterval(_.bind(this.syncMessages, this), 1000);
        },

        syncMessages: function() {
            this.collection.fetch();
        }
    });

    Views.MessageInput = Marionette.ItemView.extend({
        template: '#tpl-message-input',

        ui: {
            'input': '#message-input'
        },

        events: {
            'keydown @ui.input': 'onKeyDown'
        },

        onRender: function() {
            this.ui.input.autosize();
        },

        onKeyDown: function(e) {
            if (e.which == 13 && !e.shiftKey) {
                e.preventDefault();

                var text = this.ui.input.val();
                this.ui.input.val('');

                if (text.length) {
                    var message = {
                           'text': text,
                           'author': ChatApp.reqres.request('currentUser').get('username')
                        };

                    ChatApp.trigger('messageInput:newMessage', message);
                }
            }
        }
    });
});
