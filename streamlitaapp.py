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
def send_to_api(message: str, system_message: str, session_id: str, model_choice:str,temperature:float,maxTokens:str) -> str:
    # url = "http://172.177.31.119:3000/api/v1/prediction/ba097410-9a75-438b-90c5-3ae6c76a4ce9"
    if model_choice == "Anthropic-claude":
        url = "http://172.177.31.119:3000/api/v1/prediction/ba097410-9a75-438b-90c5-3ae6c76a4ce9"
        payload = {
        "question": message,
        "overrideConfig": {
            "systemMessagePrompt": system_message,
            "sessionId": session_id,
            "temperature":temperature,
            "max_tokens_to_sample":maxTokens
           }
        }
    if model_choice=="Azure OpenAI":
        url = "http://172.177.31.119:3000/api/v1/prediction/c6e35934-878f-4581-a77e-34c8c179594c"
        payload = {
        "question": message,
        "overrideConfig": {
            "systemMessagePrompt": system_message,
            "sessionId": session_id,
            "temperature":temperature,
            "maxTokens":maxTokens
        }
        }
    if model_choice=="Meta-llama-3":
        url="http://172.177.31.119:3000/api/v1/prediction/c0dab0c4-7610-42b2-80c7-8e169cc33124"
        payload = {
        "question": message,
        "overrideConfig": {
            "systemMessagePrompt": system_message,
            "sessionId": session_id,
            "temperature":temperature,
            "max_tokens_to_sample":maxTokens
           }
        }       
    if model_choice=="M`````````````````````````````````````````````istral-mixtral":
        url="http://172.177.31.119:3000/api/v1/prediction/c0dab0c4-7610-42b2-80c7-8e169cc33124"
        payload = {
        "question": message,
        "overrideConfig": {
            "systemMessagePrompt": system_message,
            "sessionId": session_id,
            "temperature":temperature,
            "max_tokens_to_sample":maxTokens
           }
        }       
    
    
    print("printing the payload :-",payload)
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("text", "No response from API")
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# Sidebar for system message
st.sidebar.title("System Message")
system_message = st.sidebar.text_area("Enter system message:", value="you are a helpful assistant")



model_choice = st.sidebar.selectbox("Choose API", ["Azure OpenAI", "Anthropic-claude","Meta-llama-3","Mistral-mixtral"])
temperature=st.sidebar.selectbox("select the temperature for LLM",["0","0.1","0.2","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1"])
maxTokens=st.sidebar.text_area("select the maximum token that you generate : ",value="100")
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
        assistant_response = send_to_api(prompt, system_message, st.session_state.session_id, model_choice,temperature,maxTokens)
        
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