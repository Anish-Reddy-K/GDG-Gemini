import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Set your Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY is not set in the environment variables.")
    st.stop()

client = genai.Client(api_key=api_key)

# Initialize the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Gemini Chatbot")

# Display chat messages from history
for message in st.session_state.messages:
    st.write(f"**{message['role'].capitalize()}:** {message['content']}")

# User input
user_input = st.text_input("You:", key="input")

if user_input:
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Define generation configuration
    gen_config = types.GenerateConfig(
        max_output_tokens=150,
        temperature=0.7
    )

    # Get response from Gemini
    response = client.generate(
        model="gemini-2.0-flash",
        prompt=user_input,
        config=gen_config
    )
    reply = response.candidates[0]["output"]

    # Append assistant's reply to chat history
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Display the assistant's reply
    st.write(f"**Assistant:** {reply}")
