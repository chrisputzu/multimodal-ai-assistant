import chainlit as cl
from dotenv import load_dotenv
from chainlit.types import ThreadDict
from src.select_starters import select_starter
from src.select_chat_profiles import select_chat_profile
from src.select_chat_profiles import initialize_chat_profile
from src.process_user_messages import process_user_message
from src.process_user_audios import process_audio_chunk
from src.process_user_audios import audio_answer
from src.process_user_files import handle_attachment
from src.resume_chats import resume_chat

@cl.password_auth_callback
async def password_auth_callback(username: str) -> cl.User:
    """
    Logs in and authenticates all users.

    Parameters:
    ----------
    username : str
        Username provided by the user during login.
    password : str
        Password provided by the user during login.

    Returns:
    -------
    User
        An instance of the authenticated user with admin access.
    """
    load_dotenv()
     
    return cl.User(identifier=username, metadata={'role': 'admin', 'provider': 'credentials'})
    

@cl.set_chat_profiles
async def chat_profile() -> str:    
    """
    Allows the user to select a chat profile (LLM model).

    Enables the selected model's functionalities within the chatbot. 
    Returns the selected chat profile (LLM) to be used for chatting.

    Returns:
    -------
    ChatProfile
        The chat profile (LLM) selected by the user.
    """
    return await select_chat_profile()

@cl.on_chat_start
async def on_chat_start() -> None:
    """
    Initializes the chat session with the selected chat profile.

    Sets up the session with the chosen model and returns the 
    chat session with the selected LLM.

    Parameters:
    ----------
    None
    """
    chat_profile = cl.user_session.get("chat_profile")
    await initialize_chat_profile(chat_profile=chat_profile)

@cl.set_starters
async def set_starters() -> list[str]:
    """
    Sets and returns a list of starter messages.

    These are predefined messages sent to the selected chat profile. 
    They are randomly assigned for each session.

    Returns:
    -------
    list of str
        A list of starter messages to initialize the chat.
    """
    return await select_starter()

@cl.on_audio_chunk
async def on_audio_chunk(audio_chunk: cl.AudioChunk) -> None:
    """
    Handles incoming audio chunks during user input.

    Receives audio chunks, stores the audio data in a buffer, and 
    updates the session with the buffer.

    Parameters:
    ----------
    audio_chunk : AudioChunk
        The audio chunk to process.
    """
    await process_audio_chunk(audio_chunk=audio_chunk)

@cl.on_audio_end
async def on_audio_end(elements: list) -> None:
    """
    Processes the voice message and analyzes user intent.

    Converts the audio to text using the selected chat profile. 
    Handles document analysis (file attachments) and determines 
    user intent for chatbot functionalities. Returns text and 
    voice responses depending on attached file types and user intents.

    Parameters:
    ----------
    elements : list
        A list of elements related to the audio message.
    """
    chat_profile = cl.user_session.get("chat_profile")
    model_name = await initialize_chat_profile(chat_profile=chat_profile)
    await audio_answer(elements=elements, model_name=model_name)

@cl.on_message
async def on_message(user_message: cl.Message) -> None:
    """
    Processes text messages, file attachments, and user intent.

    Handles text input, detects files in the user's message, 
    and processes them. It also interacts with the LLM chat profile 
    to respond based on the attached files and user intent for 
    chatbot functionalities.

    Parameters:
    ----------
    user_message : Message
        The incoming message with potential file attachments.
    """
    chat_profile = cl.user_session.get("chat_profile")
    await handle_attachment(user_message=user_message)
    model_name = await initialize_chat_profile(chat_profile=chat_profile)
    await process_user_message(user_message=user_message, model_name=model_name)

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict) -> None:
    """
    Resumes archived chat conversations.

    Retrieves previous chat threads to load them into memory and 
    enables users to continue a conversation.

    Parameters:
    ----------
    thread : ThreadDict
        A dictionary containing the thread's information and messages.
    """
    await resume_chat(thread=thread)
    
    
