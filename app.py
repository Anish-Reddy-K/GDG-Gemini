import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the client
client = genai.Client(api_key=api_key)

# Streamlit UI
st.title("AI Chatbot")

# Initialize session state to store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to stream response from the model
def generate_response(prompt):
    response = client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=[prompt]
    )
    for chunk in response:
        yield chunk.text

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Prompt for user input and handle response
if prompt := st.chat_input("Type your message:"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate and display assistant response
    response_container = st.chat_message("assistant")
    response_text = ""
    for chunk in generate_response(prompt):
        response_text += chunk
        # Update the response container with the latest text
        response_container.markdown(response_text + "▌")
    response_container.markdown(response_text)
    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": response_text})
