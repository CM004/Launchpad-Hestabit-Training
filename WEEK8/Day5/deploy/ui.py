import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="AI Assistant", layout="wide")

st.sidebar.header("Generation Controls")

temperature = st.sidebar.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
top_p = st.sidebar.slider("Top-p", 0.1, 1.0, 0.9, 0.05)
top_k = st.sidebar.slider("Top-k", 1, 100, 40, 1)
max_tokens = st.sidebar.slider("Max Tokens", 64, 1024, 256, 32)

mode = st.sidebar.radio("Mode", ["Chat", "Generate"])

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.session_state.chat_id = None
    st.rerun()

st.title("AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

for role, content in st.session_state.messages:
    label = "User" if role == "user" else "Assistant"
    st.markdown(f"**{label}:** {content}")

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append(("user", user_input))
    st.markdown(f"**User:** {user_input}")
    
    payload = {
        "prompt": user_input,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "max_tokens": max_tokens,
    }
    
    if mode == "Chat":
        payload["chat_id"] = st.session_state.chat_id
        endpoint = "/chat"
    else:
        endpoint = "/generate"
    
    placeholder = st.empty()
    full_response = ""
    
    response = requests.post(f"{BACKEND_URL}{endpoint}", json=payload, stream=True, timeout=60)
    
    for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
        if chunk:
            full_response += chunk
            placeholder.markdown(f"**Assistant:** {full_response}")
    
    st.session_state.messages.append(("assistant", full_response))
    
    if mode == "Chat":
        try:
            data = response.json()
            st.session_state.chat_id = data.get("chat_id")
        except Exception:
            pass
