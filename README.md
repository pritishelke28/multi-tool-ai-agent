# Multi-Tool AI Agent 🤖

An intelligent, modular AI agent built with LangChain and Streamlit. This assistant is designed to perform research, analyze private documents, and solve mathematical problems in a single, unified interface.

## 🚀 Features
* **Web Search:** Uses Tavily API to fetch real-time data from the internet.
* **Document Analysis (RAG):** Queries your local PDF files using ChromaDB and vector embeddings.
* **Math Engine:** A dedicated tool for solving complex mathematical expressions.
* **Clean UI:** A modern, chat-based interface powered by Streamlit.

## 🛠️ Project Architecture
The project follows a modular "Brain + Hands" architecture:
1.  **Agent Logic (`agent.py`):** The brain that processes user intent and selects the correct tool.
2.  **Tools (`tools/`):** Independent modules for specific tasks (Search, Calculate, RAG).
3.  **UI (`app.py`):** The Streamlit interface that interacts with the user.



## 📋 Prerequisites
* Python 3.10+
* OpenAI API Key
* Tavily API Key

