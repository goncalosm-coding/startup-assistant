import streamlit as st
from app.agents.orchestrator import run_orchestrator

st.set_page_config(
    page_title="Startup Assistant",
    page_icon="🚀",
    layout="centered"
)

st.title("🚀 Startup Assistant")
st.caption("Multi-agent AI system for startup founders. Ask me to research competitors, draft documents, or remember startup context.")

# Initialise chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about your startup..."):

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get response from orchestrator
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = run_orchestrator(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})