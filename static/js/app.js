class OpenWebUI {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.modelSelect = document.getElementById('modelSelect');
        this.temperatureSlider = document.getElementById('temperature');
        this.maxTokensSlider = document.getElementById('maxTokens');
        this.tempValue = document.getElementById('tempValue');
        this.maxTokensValue = document.getElementById('maxTokensValue');
        this.clearHistoryBtn = document.getElementById('clearHistory');
        
        this.conversation = [];
        this.isProcessing = false;
        
        this.initializeEventListeners();
        this.loadChatHistory();
    }
    
    initializeEventListeners() {
        // Send message on button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Send message on Enter key (Shift+Enter for new line)
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Update temperature display
        this.temperatureSlider.addEventListener('input', (e) => {
            this.tempValue.textContent = e.target.value;
        });
        
        // Update max tokens display
        this.maxTokensSlider.addEventListener('input', (e) => {
            this.maxTokensValue.textContent = e.target.value;
        });
        
        // Clear chat history
        this.clearHistoryBtn.addEventListener('click', () => this.clearHistory());
        
        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => {
            this.messageInput.style.height = 'auto';
            this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
        });
    }
    
    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message || this.isProcessing) return;
        
        // Add user message to conversation
        this.addMessage('user', message);
        this.conversation.push({ role: 'user', content: message });
        
        // Clear input and disable send button
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        this.sendButton.disabled = true;
        this.isProcessing = true;
        
        // Show typing indicator
        const typingIndicator = this.showTypingIndicator();
        
        try {
            // Prepare request data
            const requestData = {
                messages: this.conversation,
                model: this.modelSelect.value,
                temperature: parseFloat(this.temperatureSlider.value),
                max_tokens: parseInt(this.maxTokensSlider.value),
                stream: false
            };
            
            // Send request to API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Remove typing indicator
            typingIndicator.remove();
            
            // Add assistant response
            this.addMessage('assistant', data.response);
            this.conversation.push({ role: 'assistant', content: data.response });
            
            // Save to chat history
            this.saveChatHistory();
            
        } catch (error) {
            console.error('Error:', error);
            typingIndicator.remove();
            this.addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
        } finally {
            this.sendButton.disabled = false;
            this.isProcessing = false;
        }
    }
    
    addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
        return typingDiv;
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    saveChatHistory() {
        const history = {
            conversation: this.conversation,
            timestamp: new Date().toISOString(),
            model: this.modelSelect.value
        };
        
        localStorage.setItem('openwebui_chat_history', JSON.stringify(history));
    }
    
    loadChatHistory() {
        const saved = localStorage.getItem('openwebui_chat_history');
        if (saved) {
            try {
                const history = JSON.parse(saved);
                this.conversation = history.conversation || [];
                
                // Restore conversation display
                this.conversation.forEach(msg => {
                    this.addMessage(msg.role, msg.content);
                });
                
                // Restore model selection
                if (history.model) {
                    this.modelSelect.value = history.model;
                }
                
            } catch (error) {
                console.error('Error loading chat history:', error);
            }
        }
    }
    
    async clearHistory() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            try {
                // Clear from server
                await fetch('/api/chat/history', { method: 'DELETE' });
                
                // Clear local storage
                localStorage.removeItem('openwebui_chat_history');
                
                // Clear conversation
                this.conversation = [];
                this.chatMessages.innerHTML = '';
                
                // Show welcome message
                this.addMessage('assistant', 'Hello! I\'m your AI assistant. How can I help you today?');
                
            } catch (error) {
                console.error('Error clearing history:', error);
            }
        }
    }
    
    // WebSocket support for real-time chat (optional)
    initializeWebSocket() {
        this.ws = new WebSocket(`ws://${window.location.host}/ws/chat`);
        
        this.ws.onopen = () => {
            console.log('WebSocket connected');
        };
        
        this.ws.onmessage = (event) => {
            // Handle streaming responses
            console.log('WebSocket message:', event.data);
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new OpenWebUI();
    
    // Add welcome message
    if (app.conversation.length === 0) {
        app.addMessage('assistant', 'Hello! I\'m your AI assistant. How can I help you today?');
    }
    
    // Optional: Initialize WebSocket for real-time features
    // app.initializeWebSocket();
});

// Add some utility functions
function formatTimestamp(timestamp) {
    return new Date(timestamp).toLocaleString();
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Show a brief "copied" message
        const notification = document.createElement('div');
        notification.textContent = 'Copied to clipboard!';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 2000);
    });
}

// Add CSS animation for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
