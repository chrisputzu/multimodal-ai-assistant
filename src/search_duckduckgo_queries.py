import chainlit as cl
from duckduckgo_search import AsyncDDGS

async def agent_results_text(user_message: str) -> list[dict[str, str, str]]:
    """
    Asynchronously retrieves text search results from DuckDuckGo based on user input.

    Args:
        user_message (str): The query string entered by the user.

    Returns:
        list[dict]: A list of search result dictionaries containing information like title, link, and description.
    """
    results = await AsyncDDGS().text(keywords=user_message, max_results=10)

    return results

async def text(
    keywords: str,
    max_results: int | None = None,
    ) -> list[dict[str, str, str]]:
    """
    Performs a text search on DuckDuckGo with specified query parameters.

    Args:
        keywords (str): The search keywords.
        max_results (int | None): Maximum number of results to retrieve. If None, defaults to the first response only.

    Returns:
        list[dict]: A list of dictionaries containing the search results.
    """
    results_text = AsyncDDGS().text(keywords=keywords,  max_results=10)
    
    return results_text




