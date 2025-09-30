# ui.py
import re
import streamlit as st
from agent import get_agent_response

st.set_page_config(page_title="LangChain Chat Agent", layout="wide")

st.title("💬 LangChain Chat Agent")

# -----------------------
# Initialize chat history
# -----------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "text": "Hi — I'm your LangChain agent. Ask me anything!"}
    ]

# -----------------------
# Display chat history
# -----------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        text = msg["text"]
        # Show all YouTube links
        yt_links = re.findall(r"(https?://www\.youtube\.com/watch\?v=[\w-]+)", text)
        for link in yt_links:
            col, _ = st.columns([2, 3])
            with col:
                st.video(link)
            text = text.replace(link, "")
            
        # # Show leftover plain text
        if text.strip():
            st.markdown(text)

# -----------------------
# Input box at bottom
# -----------------------
if user_input := st.chat_input("Type your message..."):
    # User message
    st.session_state.messages.append({"role": "user", "text": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Agent response with spinner
    with st.spinner(" Thinking..."):
        try:
            response = get_agent_response(user_input)
        except Exception as e:
            response = f"Agent error: {e}"

    st.session_state.messages.append({"role": "assistant", "text": response})
    with st.chat_message("assistant"):
        text = response
        yt_links = re.findall(r"(https?://www\.youtube\.com/watch\?v=[\w-]+)", text)
        for link in yt_links:
            col, _ = st.columns([2, 3])
            with col:
                st.video(link)
            text = text.replace(link, "")
            
        if text.strip():
            st.markdown(text)