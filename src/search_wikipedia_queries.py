import wikipedia

async def search_wikipedia_query(user_message: str) -> tuple[str, str]:
    """
    Retrieves the URL and content of a Wikipedia page for the given query.

    Args:
        user_query (str): The title or topic to search for on Wikipedia.

    Returns:
        tuple: A tuple containing the page URL and its content.
    """
    result_query = wikipedia.page(user_message)
    url = result_query.url
    
    content = result_query.content
    
    return url, content
    
    
    
    