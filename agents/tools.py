from langchain.tools import tool, Tool
from langchain_community.utilities import SerpAPIWrapper, DuckDuckGoSearchAPIWrapper, GoogleSerperAPIWrapper
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
from tavily import TavilyClient
from typing import Dict, Any,List


# Initialize the external tools
tavily = TavilySearchResults(max_results=3)
params = {"engine": "google", "gl": "us", "hl": "en"}
serpapi = SerpAPIWrapper(params=params)
duckduckgo = DuckDuckGoSearchAPIWrapper()
wikipedia = WikipediaAPIWrapper()
google_search = GoogleSerperAPIWrapper()


class SearchTools:
    @staticmethod
    @tool
    def search_tavily(query: str) -> str:
        """
        Searches for the given query using TavilyClient.

        Args:
            query: The search query

        Returns:
            str: Search results content
        """
        client = TavilyClient()
        response = client.search(query, max_results=3, search_depth="Advanced")
        return response['results']
    
    # @staticmethod
    # @tool
    # def search_tavily(query: str) -> str:
    #     """
    #     Searches for the given query using TavilySearchResults.

    #     Args:
    #         query: The search query

    #     Returns:
    #         str: Search results content
    #     """
    #     return SearchTools.tavily.run(query)

    # @staticmethod
    # @tool
    # def search_serpapi(query: str) -> str:
    #     """
    #     Searches using SerpAPI.

    #     Args:
    #         query: The search query

    #     Returns:
    #         str: Search results content
    #     """
    #     return SearchTools.serpapi.run(query)

    # @staticmethod
    # @tool
    # def search_duckduckgo(query: str) -> str:
    #     """
    #     Searches using DuckDuckGo.

    #     Args:
    #         query: The search query

    #     Returns:
    #         str: Search results content
    #     """
    #     return SearchTools.duckduckgo.run(query)

    # @staticmethod
    # @tool
    # def search_wikipedia(query: str) -> str:
    #     """
    #     Searches Wikipedia for the given query.

    #     Args:
    #         query: The search query

    #     Returns:
    #         str: Search results content
    #     """
    #     return SearchTools.wikipedia.run(query)

    # @staticmethod
    # @tool
    # def search_google(query: str) -> str:
    #     """
    #     Searches using Google Search.

    #     Args:
    #         query: The search query

    #     Returns:
    #         str: Search results content
    #     """
    #     return SearchTools.google_search.run(query)

    @staticmethod
    def get_tool_list():
        """
        Returns the list of available tools.

        Returns:
            list: List of tool instances
        """
        return [SearchTools.search_tavily,
            Tool(
        name="SerpAPI",
        func= serpapi.run,
        description="A powerful web search tool that provides comprehensive results from Google. Use this for general queries, fact-checking, and finding up-to-date information on a wide range of topics. It's particularly useful for current events, popular culture, and general knowledge questions.",
    ),
    Tool(
        name="DuckDuckGo Search",
        func=duckduckgo.run,
        description="A privacy-focused search engine that offers unbiased results. Use this tool when you need to find information on topics that might be controversial or when you want to avoid personalized search results. It's excellent for gathering diverse viewpoints and alternative sources.",
    ),
    Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="An extensive online encyclopedia that provides detailed background information on a vast array of topics. Use this tool when you need in-depth explanations, historical context, or comprehensive overviews of subjects. It's particularly useful for academic topics, biographies, and understanding complex concepts.",
    ),
    Tool(
        name="Tavily Search",
        func=tavily.run,
        description="Use when you to serach the web"
    ),
    Tool(
        name="Google Search",
        func=google_search.run,
        description="Use when you to serach the web"
    ),
]
