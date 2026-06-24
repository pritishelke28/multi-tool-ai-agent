import streamlit as st
from agent import agent_executor

# Page configuration
st.set_page_config(page_title="Multi-Tool AI Agent", layout="centered")

st.title("🤖 Multi-Tool AI Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Call the agent_executor from agent.py
                response = agent_executor.invoke({"input": prompt})
                output = response["output"]
                st.markdown(output)
                st.session_state.messages.append({"role": "assistant", "content": output})
            except Exception as e:
                st.error(f"An error occurred: {e}")