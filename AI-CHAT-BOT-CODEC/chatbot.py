
from flask import Flask, request, jsonify, render_template_string
import json
import random
import re

app = Flask(__name__)

class BasicChatBot:
    def __init__(self):
        self.responses = {
            "hello": [
                "Hi there! How can I help you?",
                "Hello! What's on your mind?",
                "Hey! I'm here to chat with you."
            ],
            "how_are_you": [
                "I'm doing great, thanks for asking!",
                "I'm good! How are you doing?",
                "All good here! What about you?"
            ],
            "name": [
                "I'm ChatBot, your friendly AI assistant!",
                "You can call me ChatBot. What's your name?",
                "I'm ChatBot. Nice to meet you!"
            ],
            "help": [
                "I can chat with you about various topics!",
                "Just talk to me - I'll do my best to respond!",
                "Ask me anything and I'll try to help!"
            ],
            "goodbye": [
                "Goodbye! Have a wonderful day!",
                "See you later! Take care!",
                "Bye! It was nice chatting with you!"
            ],
            "thanks": [
                "You're welcome!",
                "Happy to help!",
                "No problem at all!"
            ],
            "default": [
                "That's interesting! Tell me more.",
                "I see. Can you explain that differently?",
                "Hmm, I'm not sure about that. What else would you like to know?",
                "Interesting question! What made you think of that?"
            ]
        }
    
    def get_intent(self, message):
        """Simple keyword matching to understand what user wants"""
        message = message.lower().strip()
        

        if any(word in message for word in ['hello', 'hi', 'hey', 'good morning']):
            return "hello"
        

        if any(phrase in message for phrase in ['how are you', 'how r u', 'how do you do']):
            return "how_are_you"

        if any(phrase in message for phrase in ['your name', 'who are you', 'what are you']):
            return "name"
        

        if any(word in message for word in ['help', 'assist', 'support']):
            return "help"
        

        if any(word in message for word in ['bye', 'goodbye', 'see you', 'exit']):
            return "goodbye"
        

        if any(word in message for word in ['thank', 'thanks', 'appreciate']):
            return "thanks"
        

        return "default"
    
    def get_response(self, message):
        """Get response based on user message"""
        intent = self.get_intent(message)
        possible_responses = self.responses[intent]
        return random.choice(possible_responses)


chatbot = BasicChatBot()


CHAT_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Simple Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .chat-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .chat-box {
            height: 400px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            overflow-y: auto;
            background-color: #fafafa;
            margin-bottom: 15px;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 15px;
            max-width: 70%;
        }
        .user-message {
            background-color: #007bff;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        .bot-message {
            background-color: #e9ecef;
            color: #333;
        }
        .input-area {
            display: flex;
            gap: 10px;
        }
        .input-area input {
            flex: 1;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            outline: none;
            font-size: 16px;
        }
        .input-area input:focus {
            border-color: #007bff;
        }
        .input-area button {
            padding: 12px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
        }
        .input-area button:hover {
            background-color: #0056b3;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .typing {
            color: #666;
            font-style: italic;
            padding: 5px 15px;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>🤖 Simple Chatbot</h1>
        <div class="chat-box" id="chatBox">
            <div class="message bot-message">
                Hello! I'm your chatbot. Type anything to start our conversation!
            </div>
        </div>
        <div class="input-area">
            <input type="text" id="userInput" placeholder="Type your message here..." 
                   onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function addMessage(message, isUser) {
            const chatBox = document.getElementById('chatBox');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + (isUser ? 'user-message' : 'bot-message');
            messageDiv.textContent = message;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        function showTyping() {
            const chatBox = document.getElementById('chatBox');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'typing';
            typingDiv.id = 'typing';
            typingDiv.textContent = 'Bot is typing...';
            chatBox.appendChild(typingDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
        function removeTyping() {
            const typing = document.getElementById('typing');
            if (typing) typing.remove();
        }
        
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            
            if (message === '') return;
            
            // Add user message
            addMessage(message, true);
            input.value = '';
            
            // Show typing indicator
            showTyping();
            
            try {
                // Send to server
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({message: message})
                });
                
                const data = await response.json();
                
                // Remove typing and add bot response
                setTimeout(() => {
                    removeTyping();
                    addMessage(data.response, false);
                }, 1000); // Small delay for realism
                
            } catch (error) {
                removeTyping();
                addMessage('Sorry, something went wrong!', false);
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    """Main chat page"""
    return render_template_string(CHAT_HTML)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        user_message = data['message']
        

        bot_response = chatbot.get_response(user_message)
        
        return jsonify({
            'response': bot_response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'response': 'Sorry, I had trouble understanding that.',
            'status': 'error'
        }), 500


@app.route('/secret')
def secret():
    """Hidden page for developers"""
    return """
    <h1> Developer Easter Egg Found!</h1>
    <p>Congratulations! You found the secret developer page!</p>
    <p>🚀 Your chatbot is running smoothly!</p>
    <p><a href="/">Back to Chat</a></p>
    """

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 SIMPLE CHATBOT STARTING...")
    print("=" * 50)
    print("📱 Chat here: http://localhost:5000")
    print("🎉 Secret page: http://localhost:5000/secret")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)