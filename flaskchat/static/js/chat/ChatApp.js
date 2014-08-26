'use strict';

window.ChatApp = new Backbone.Marionette.Application();

ChatApp.addRegions({
    'usersRegion': '#users-region',
    'chatMessagesRegion': '#chat-messages-region',
    'messageInputRegion': '#message-input-region'
});

ChatApp.addInitializer(function(options) {
    var users = new ChatApp.Views.UserList({
            'collection': options.users
        }),
        messages = new ChatApp.Views.ChatMessageList({
            'collection': options.messages,
            'chatId': options.chatId
        }),
        input = new ChatApp.Views.MessageInput();

    ChatApp.reqres.setHandler('currentUser', function() {
        return options.currentUser;
    });

    ChatApp.usersRegion.show(users);
    ChatApp.chatMessagesRegion.show(messages);
    ChatApp.messageInputRegion.show(input);
});
