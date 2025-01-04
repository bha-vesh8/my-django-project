const chatbotSend = document.getElementById('chatbotSend');
const chatbotInput = document.getElementById('chatbotInput');
const chatbotMessages = document.getElementById('chatbotMessages');

chatbotSend.addEventListener('click', () => {
    const userMessage = chatbotInput.value;
    if (userMessage.trim() !== '') {
        // Display user message
        const userMessageDiv = document.createElement('div');
        userMessageDiv.textContent = 'You: ' + userMessage;
        chatbotMessages.appendChild(userMessageDiv);

        // Clear input field
        chatbotInput.value = '';

        // Send the message to Django backend
        fetch(`/chatbot/chatbot-response/?message=${encodeURIComponent(userMessage)}`)
            .then(response => response.json())
            .then(data => {
                // Display bot response
                const botResponseDiv = document.createElement('div');
                botResponseDiv.textContent = 'Bot: ' + data.response;
                chatbotMessages.appendChild(botResponseDiv);

                // Scroll to the latest message
                chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});