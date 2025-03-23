document.getElementById('send-button').addEventListener('click', function () {
    sendMessage();
});

document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput) return;

    // Add user's message to the chat box
    appendMessage('You', userInput);

    // Clear the input field
    document.getElementById('user-input').value = '';

    // Send the message to the backend
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Add chatbot's response to the chat box
        appendMessage('Chatbot', data.response);
    })
    .catch(error => {
        console.error('Error:', error);
        appendMessage('Chatbot', 'Sorry, something went wrong. Please try again.');
    });
}

function appendMessage(sender, message) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
}