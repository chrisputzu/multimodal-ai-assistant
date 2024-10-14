import chainlit as cl
from pandas import DataFrame
from langchain_community.chat_models import ChatOllama
from src.generate_images import generate_image
from src.search_wikipedia_queries import search_wikipedia_query
from src.topic_classifier import classify_intent
from src.scrape_links import scrape_link
from src.search_duckduckgo_queries import agent_results_text

async def process_user_message(user_message: cl.Message, model_name: str) -> None:
    """
    Processes a user message and provides a response using a language model or performs specific actions based on the intent.

    Args:
        user_message (cl.Message): The message sent by the user to be processed.
        model_name (str): The model selected with the chat_profile choice.

    Workflow:
    - If no active chain exists in the user session:
        1. Classifies the user's intent (image generation, Wikipedia search, web scraping, or general chat).
        2. Executes the corresponding action:
            - Generates an image (if 'image' intent).
            - Searches Wikipedia (if 'wikipedia' intent).
            - Scrapes content from a URL (if 'scraper' intent).
            - Searches using DuckDuckGo (if 'search' intent).
            - Answers a general chat question (if 'chat' intent).

    - If an active chain exists:
        - Processes the message using the existing chain and retrieves the response and source documents.
    """
    chain = cl.user_session.get("chain")
    user_message = user_message.content.strip()

    if chain is None:
        intent = await classify_intent(user_message=user_message)
        
        if 'image' in intent:
            print('Your intent is: ', intent)
            
            await cl.Message(content="🖼️ Image Generation Selected! 🖼️ \n You've chosen to generate an image. Please note that if you don't have a GPU, the CUDA option won't be available, and it may take up to 15 minutes to generate a 512x512 image.").send()
            
            generated_image_path = await generate_image(user_message=user_message)
            image_element = cl.Image(name="Generated Image", path=generated_image_path)
            
            await cl.Message(content="✨ Here you go! ✨ \n Here’s the generated image!", elements=[image_element]).send()
            
        elif 'wikipedia' in intent:
            print('Your intent is: ', intent)

            query = user_message.split(' ')[1:]
            keywords_string = ''.join(query)
            
            await cl.Message(content="🔍 Wikipedia Search Selected! 🔍\n You've chosen to search on Wikipedia. Please enter your topic in the form of keywords below!").send()
            
            url, content = await search_wikipedia_query(user_message=keywords_string)
            formatted_results = f"🔗 **Source Link:** {url}\n\n📖 **Content:** {content}"
            
            await cl.Message(content=formatted_results).send()
        
        elif 'scraper' in intent:
            print('Your intent is: ', intent)

            scraped_link = await scrape_link(user_message=user_message)
            link_element = cl.File(name='Extracted link', path=str(scraped_link))
            
            await cl.Message(content='🎉 Your link has been successfully extracted 🎉.\n Click here to access the content directly!: ', elements=[link_element]).send()
            
        elif 'search' in intent:
            print('Your intent is: ', intent)
                        
            await cl.Message(content="🌐 DuckDuckGo Search Selected! 🌐 \n You've chosen to search on the DuckDuckGo Web Browser.\n The first 10 links will be displayed.").send()
            search_results = await agent_results_text(user_message=user_message)

            formatted_results = ""
            for index, result in enumerate(search_results[:10], start=1):  
                title = result['title']
                href = result['href']
                body = result['body']
                formatted_results += f"{index}. **Title:** {title}\n**Link:** {href}\n**Description:** {body}\n\n"

            await cl.Message(content=formatted_results).send()
                          
        elif 'chat' in intent:
            print('Your intent is: ', intent)
                
            model = ChatOllama(model=model_name) 
            answer = await model.ainvoke(user_message)
            
            await cl.Message(content=answer.content).send()

    else:
        if type(chain) == str:
            pass
            
        elif type(chain) == DataFrame:
            pass

        else:  
            response = await chain.ainvoke(user_message)
            answer = response["answer"]
            
            await cl.Message(content=answer).send()
