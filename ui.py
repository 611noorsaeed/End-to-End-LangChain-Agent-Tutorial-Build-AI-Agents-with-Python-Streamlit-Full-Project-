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
# Helper: render message
# -----------------------
def render_message(role, text):
    with st.chat_message(role):
        rendered = False

        # Show all YouTube links (reduced size using column)
        yt_links = re.findall(r"(https?://www\.youtube\.com/watch\?v=[\w-]+)", text)
        for link in yt_links:
            col, _ = st.columns([2, 3])  # make it ~40% width
            with col:
                st.video(link)
            text = text.replace(link, "")
            rendered = True

        # Show all image links
        img_links = re.findall(r"(https?://[^\s]+\.(?:png|jpg|jpeg|gif))", text)
        for link in img_links:
            st.image(link, use_column_width=True)
            text = text.replace(link, "")
            rendered = True

        # Show other links as markdown
        url_links = re.findall(r"(https?://[^\s]+)", text)
        for link in url_links:
            st.markdown(f"[{link}]({link})")
            text = text.replace(link, "")
            rendered = True

        # Show leftover plain text
        if text.strip():
            st.write(text)
            rendered = True

        if not rendered:
            st.write(text)


# -----------------------
# Display chat history
# -----------------------
for msg in st.session_state.messages:
    render_message(msg["role"], msg["text"])


# -----------------------
# Input box at bottom
# -----------------------
if user_input := st.chat_input("Type your message..."):
    # User message
    st.session_state.messages.append({"role": "user", "text": user_input})
    render_message("user", user_input)

    # Agent response with spinner
    with st.spinner(" Thinking..."):
        try:
            response = get_agent_response(user_input)
        except Exception as e:
            response = f"Agent error: {e}"

    st.session_state.messages.append({"role": "assistant", "text": response})
    render_message("assistant", response)