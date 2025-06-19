document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    const maximizeBtn = document.getElementById('maximizeBtn');
    const card = document.querySelector('.card');

    // Function to scroll to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to add a message to the chat
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'message user-message' : 'message bot-message';
        messageDiv.innerHTML = `<div class="message-content">${message}</div>`;
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    // Show welcome message when page loads
    async function showWelcomeMessage() {
        try {
            const response = await fetch('/welcome');
            const data = await response.json();
            addMessage(data.response);
        } catch (error) {
            console.error('Error loading welcome message:', error);
            addMessage('Welcome to AI PDPA Chat! How can I help you today?');
        }
    }

    // Call showWelcomeMessage when page loads
    showWelcomeMessage();

    // Handle form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        const provider = document.getElementById('llm-model').value;
        if (!message) return;

        // Add user message
        addMessage(message, true);
        
        // Clear input
        messageInput.value = '';
        
        // Show loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot-message';
        loadingDiv.innerHTML = '<div class="message-content"><div class="loading"></div></div>';
        chatMessages.appendChild(loadingDiv);
        scrollToBottom();
        
        try {
            const response = await fetch('/langchain', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: message,
                    provider: provider
                })
            });
            
            const data = await response.json();
            
            // Remove loading indicator
            chatMessages.removeChild(loadingDiv);
            
            if (response.ok) {
                // Add bot response
                addMessage(data.response);
            } else {
                alert(data.error || "Sorry, there was an error processing your request.");
            }
            
        } catch (error) {
            console.error('Error:', error);
            chatMessages.removeChild(loadingDiv);
            addMessage('Sorry, there was an error processing your request.');
        }
    });

    // Handle maximize/minimize
    maximizeBtn.addEventListener('click', function() {
        card.classList.toggle('maximized');
        maximizeBtn.innerHTML = card.classList.contains('maximized') ? 
            '<i class="fas fa-compress"></i>' : 
            '<i class="fas fa-expand"></i>';
        
        // Scroll to bottom after maximizing/minimizing
        setTimeout(scrollToBottom, 100);
    });

    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Handle Enter key
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // Handle window resize
    window.addEventListener('resize', function() {
        scrollToBottom();
    });

    // Initial scroll to bottom
    scrollToBottom();
}); 