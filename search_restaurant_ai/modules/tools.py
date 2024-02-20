from typing import Any

from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults


@tool("tavily-search")
def tavily_search_tool(query: str) -> Any:
    """Tavily Search"""
    return TavilySearchResults().invoke(query)
