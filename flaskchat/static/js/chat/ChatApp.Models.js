'use strict';

ChatApp.module('Models', function(Models, App, Backbone) {
    Models.User = Backbone.Model.extend({
        defaults: {
            'username': ''
        }
    });

    Models.ChatMessage = Backbone.Model.extend({
        defaults: {
            'text': '',
            'author': '',
            'created_at': 0,
        },

        initialize: function () {
            if (this.isNew()) {
                this.set('created_at', Date.now());
            }
        }
    })

    Models.UserList = Backbone.Collection.extend({
        url: function() {return '/api/chat/' + CHAT_ID + '/users'},
        model: Models.User,

        comparator: 'username',

        parse: function(response) {
            return response.result;
        }
    })

    Models.ChatMessageList = Backbone.Collection.extend({
        url: function() {return '/api/chat/' + CHAT_ID + '/messages'},
        model: Models.ChatMessage,

        comparator: 'created_at',

        parse: function(response) {
            return response.result;
        }
    })
});
