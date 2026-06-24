import os
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# 1. Initialize the Groq LLM
# Ensure GROQ_API_KEY is set in your environment or Streamlit secrets
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0
)

# 2. Initialize the Tavily Search Tool
# Ensure TAVILY_API_KEY is set in your environment
search_tool = TavilySearchResults(max_results=3)
tools = [search_tool]

# 3. Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful research assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 4. Create the agent and executor
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)