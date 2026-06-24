# F:\multi-tool-ai-agent\tools\search.py
from langchain_community.tools.tavily_search import TavilySearchResults
import os

# Ensure the API key is loaded
# If you are using python-dotenv, make sure load_dotenv() is called in main.py
search_tool = TavilySearchResults(max_results=3)
