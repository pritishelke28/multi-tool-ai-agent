import streamlit as st
from agent import agent_executor

st.set_page_config(page_title="My AI Assistant", layout="centered")

st.title("My AI Assistant")
st.markdown("Ask me anything about your documents, web facts, or math.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show messages

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle user input
if prompt := st.chat_input("Enter your query here..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Run agent
    response = agent_executor.invoke({"input": prompt})
    answer = response["output"]
    
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})