import chainlit as cl
from chainlit.types import ThreadDict
from langchain.memory import ConversationBufferMemory
    
async def resume_chat(thread: ThreadDict) -> None:    
    """
    Retrieve an archived chat and allow the user to continue the conversation.

    Args:
        thread (ThreadDict): A dictionary containing messages and their details.

    Returns:
        None
    """
    memory = ConversationBufferMemory(return_messages=True)
    root_messages = [m for m in thread["steps"] if m["parentId"] is None]
    
    for message in root_messages:
        if message["type"] == "user_message":
            memory.chat_memory.add_user_message(message["output"])
        else:
            memory.chat_memory.add_ai_message(message["output"])

    cl.user_session.set("memory", memory)