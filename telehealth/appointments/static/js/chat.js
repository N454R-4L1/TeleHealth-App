document.getElementById('chat-send').onclick = function() {
    var input = document.getElementById('chat-input');
    var message = input.value.trim();
    if (message) {
        var chatWindow = document.getElementById('chat-window');
        var newMessage = document.createElement('div');
        newMessage.textContent = message;
        chatWindow.appendChild(newMessage);
        input.value = '';
    }
};
