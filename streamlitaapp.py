import streamlit as st
import requests
import time
import uuid

# Set page title
st.set_page_config(page_title="Softtek Demo Chat")

# Initialize session state for chat history and session ID if they don't exist
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Function to send request to API
def send_to_api(message: str, system_message: str, session_id: str) -> str:
    url = "http://172.177.31.119:3000/api/v1/prediction/ba097410-9a75-438b-90c5-3ae6c76a4ce9"
    payload = {
        "question": message,
        "overrideConfig": {
            "systemMessagePrompt": system_message,
            "sessionId": session_id
        }
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("text", "No response from API")
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Sidebar for system message
st.sidebar.title("System Message")
system_message = st.sidebar.text_area("Enter system message:", value="you are a helpful assistant")

# Display session ID (you can remove this in production)
st.sidebar.text(f"Session ID: {st.session_state.session_id}")

# Main chat interface
st.title("Softtek Demo Chat")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is your question?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = send_to_api(prompt, system_message, st.session_state.session_id)
        
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

st.sidebar.markdown("---")
st.sidebar.markdown("Note: The system message affects how the AI responds to your questions.")