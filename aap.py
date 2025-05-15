import streamlit as st
import requests

# App Title
st.title('Groq-Powered LLM Chatbot')

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Input field for user message
user_input = st.text_input('You:', placeholder='Type your message here...')

# Display the chat history
for message in st.session_state.history:
    if message['role'] == 'user':
        st.write(f'You: {message["content"]}')
    else:
        st.write(f'Bot: {message["content"]}')

# Send button logic
if st.button('Send'):
    if user_input:
        # Append user's message to history
        st.session_state.history.append({'role': 'user', 'content': user_input})

        # === Groq API Integration ===
        try:
            response = requests.post(
                "https://api.groq.com/v1/chat/completions",
                headers={"Authorization": "Bearer YOUR_GROQ_API_KEY"},
                json={
                    "model": "groq-llm", 
                    "messages": [{"role": "user", "content": user_input}]
                }
            )
            bot_response = response.json().get('choices', [{}])[0].get('message', {}).get('content', "Groq API did not return a response.")
        except Exception as e:
            bot_response = f"Error contacting Groq API: {str(e)}"
        
        # Append bot's response to history
        st.session_state.history.append({'role': 'bot', 'content': bot_response})

        # Clear the input field after sending
        st.experimental_rerun()
