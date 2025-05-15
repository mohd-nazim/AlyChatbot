import streamlit as st
from datetime import datetime
import requests

# Initialize the app
st.set_page_config(page_title='LLM Chatbot', layout='centered')
st.title('💬 LLM Chatbot')

# API Key input (you can replace this with a config file or env variable)
api_key = st.text_input('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', type='Abcd+1234')

# Groq API URL
api_url = 'https://api.groq.com/v1/chat/completion'

# Maintain conversation history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# User input
user_input = st.text_input('You:', placeholder='Type your message...')

# Send button logic
if st.button('Send') and user_input:
    # Store user message
    st.session_state['messages'].append(('You', user_input))
    
    # Call Groq API
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    data = {
        'messages': [{'role': 'user', 'content': user_input}]
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        if response.status_code == 200:
            bot_reply = response.json().get('choices')[0].get('message').get('content')
        else:
            bot_reply = f'Error: {response.status_code} - {response.text}'
    except Exception as e:
        bot_reply = f'Error: {e}'

    # Store bot response
    st.session_state['messages'].append(('Bot', bot_reply))

# Display the conversation
for sender, message in st.session_state['messages']:
    if sender == 'You':
        st.markdown(f'**You:** {message}')
    else:
        st.markdown(f'**Bot:** {message}')
