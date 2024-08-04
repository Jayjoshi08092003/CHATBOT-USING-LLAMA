import os
import json

import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Chatbot using LLM",
    page_icon="🇦🇮",
    layout="centered"
)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(working_dir, "config.json")

with open(config_path, "r") as config_file:
    config_data = json.load(config_file)

GROQ_API_KEY = config_data.get("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Initialize chat history in session state if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit page title
st.title("Chatbot using LLM")

# Display the chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for the user's prompt
user_prompt = st.chat_input("Ask LLM...")

if user_prompt:
    # Display the user's message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Prepare messages for the LLM
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]

    # Get response from the LLM
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # Display the assistant's message
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
