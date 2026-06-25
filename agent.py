import os
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Initialize Tools
search_tool = TavilySearchResults(max_results=3)
tools = [search_tool]

# Initialize Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful research assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# Initialize Agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)