from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# 1. Initialize the Groq LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile", # You can pick other models like 'llama-3.1-8b-instant'
    temperature=0
)

# 2. Initialize the Tavily Tool
search_tool = TavilySearchResults(max_results=3)
tools = [search_tool]

# 3. Create the agent (same structure as before)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful research assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)