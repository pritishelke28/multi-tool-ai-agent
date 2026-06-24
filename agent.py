# 1. ALWAYS PUT IMPORTS AT THE TOP
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are 'MyAgent', a custom research assistant. "
               "You have access to: 1) Local PDFs for document analysis, "
               "2) Web Search for real-time data, and 3) a Calculator for math. "
               "If a user asks about documents, use the query_documents tool. "
               "If a user asks for live facts, use the search_tool."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])
