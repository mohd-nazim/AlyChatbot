import streamlit as st
import requests
import os
from dotenv import load_dotenv

# ✅ Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# ✅ Environment variables
GROQ_API_URL = os.getenv("GROQ_API_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

st.title("Document Research & Theme Identification Chatbot by Mohd Nazim")

user_input = st.text_input("Ask something about your documents:")

if st.button("Send"):
    if user_input:
        if not GROQ_API_URL or not GROQ_API_KEY:
            st.error("API URL or API Key is missing. Please check your .env file.")
        else:
            st.write("Sending request to Groq API...")  
            try:
                # ✅ Direct API call to Groq
                response = requests.post(
                    GROQ_API_URL,
                    headers={
                        "Authorization": f"Bearer {GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "user", "content": user_input}
                        ]
                    }
                )

                # ✅ Response Handling
                st.write("Response Status Code:", response.status_code)  
                st.write("Response Text:", response.text)               

                if response.status_code == 200:
                    data = response.json()
                    # ✅ Correct path to extract the message
                    reply = data["choices"][0]["message"]["content"]
                    st.write("**Bot:**", reply)
                else:
                    st.error(f"Failed to connect: {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"❌ **Exception Occurred:** {str(e)}")
    else:
        st.warning("Please type a message before sending.")
