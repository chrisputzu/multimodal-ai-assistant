import chainlit as cl
import PyPDF2
import docx
import base64
import datahorse as dh
import pandas as pd
from io import BytesIO
from PIL import Image
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from src.create_chain_retrievers import create_chain_retriever
from src.process_text_to_speech import speak_async

async def process_pdf(file: cl.File) -> ConversationalRetrievalChain:
    """
    Processes a PDF file to extract text and create a conversational retrieval chain.

    Extracts text from each page of the PDF and passes it to the `create_chain_retriever` 
    function for further processing. Sends a message to the user informing them of the task.

    Parameters:
    ----------
    file : File
        The PDF file to be processed.

    Returns:
    -------
    ConversationalRetrievalChain
        An instance of the conversational retrieval chain created from the 
        extracted text.
    """
    await cl.Message(content=f"📄✨ Processing the PDF file: **`{file.name}`**... Please hold on! ⏳").send()

    pdf = PyPDF2.PdfReader(file.path)
    pdf_text = ""
    for page in pdf.pages:
        pdf_text += page.extract_text()
        
    return await create_chain_retriever(texts=pdf_text, source_prefix="pdf")

async def process_txt(file: cl.File) -> ConversationalRetrievalChain:
    """
    Processes a text file to create a conversational retrieval chain.

    Reads the contents of the file and sends the text to the `create_chain_retriever`
    for further processing. Notifies the user of the progress.

    Parameters:
    ----------
    file : File
        The text file to be processed.

    Returns:
    -------
    ConversationalRetrievalChain
        A conversational retrieval chain created from the extracted text.
    """
    await cl.Message(content=f"📜✨🐍 Processing the text/python file: **`{file.name}`**... Please wait a moment! ⏳").send()

    with open(file.path, "r", encoding="utf-8") as txt_file:
        txt_text = txt_file.read()
        
    return await create_chain_retriever(texts=txt_text, source_prefix="txt")

async def process_word(file: cl.File) -> ConversationalRetrievalChain:
    """
    Processes a Word document to create a conversational retrieval chain.

    Extracts text from the Word document's paragraphs and passes it to the 
    `create_chain_retriever` function. Sends a message notifying the user.

    Parameters:
    ----------
    file : File
        The Word document to be processed.

    Returns:
    -------
    ConversationalRetrievalChain
        A conversational retrieval chain created from the document's text.
    """
    await cl.Message(content=f"📄📝 Processing the Word document: **`{file.name}`**... Please wait! ⏳").send()
    
    doc = docx.Document(file.path)
    doc_text = "\n".join([para.text for para in doc.paragraphs])
    
    return await create_chain_retriever(texts=doc_text, source_prefix="docx")

async def process_python(file: cl.File) -> ConversationalRetrievalChain:
    """
    Processes a Python file to create a conversational retrieval chain.

    Processes the Python file similarly to a text file using `process_txt`. 
    Sends a notification about the task to the user.

    Parameters:
    ----------
    file : File
        The Python file to be processed.

    Returns:
    -------
    ConversationalRetrievalChain
        A conversational retrieval chain created from the Python file.
    """
    return await process_txt(file=file)

def prompt_func(data: dict) -> list:
    """
    Creates a formatted message for the chat model using text and image data.

    Formats the input data into a structure suitable for the 
    chat model, combining both text and image components.

    Parameters:
    ----------
    data : dict
        A dictionary containing the keys "text" and "image", where "text" 
        is the textual content and "image" is a base64 encoded image string.

    Returns:
    -------
    list
        A list containing a HumanMessage formatted with the combined text 
        and image data.
    """
    text = data["text"]
    image = data["image"]

    image_part = {
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{image}",
    }

    content_parts = []
    text_part = {"type": "text", "text": text}
    content_parts.append(image_part)
    content_parts.append(text_part)
    
    human_message = [HumanMessage(content=content_parts)]

    return human_message

async def process_img(file: cl.File, user_message: str) -> str:
    """
    Processes an image file and generates a description.

    Converts the image to a base64-encoded string and uses a chat model to describe it.
    Notifies the user about the task and sends the generated description.

    Parameters:
    ----------
    file : File
        The image file to be processed.

    Returns:
    -------
    str
        A description of the image generated by the chat model.
    """
    await cl.Message(content=f"🖼️ Processing your image file '{file.name}'... Please hold on while i work on it!").send()
    
    pil_image = Image.open(file.path)
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    llm = ChatOllama(model="llava-llama3")
    chain = prompt_func | llm | StrOutputParser()
    answer_chain = await chain.ainvoke({"text": user_message, "image": img_str_b64})
    
    await cl.Message(content=answer_chain).send()
        
    return answer_chain

async def process_csv(file: cl.File) -> pd.DataFrame:
    """
    Processes a CSV file to create a smart DataFrame agent.

    Reads the file into a DataFrame using the `datahorse` library, then
    sends a notification to the user about the task.

    Parameters:
    ----------
    file : File
        The CSV file to be processed.

    Returns:
    -------
    DataFrame
        A DataFrame agent created from the file data.
    """
    await cl.Message(content=f"📊 Processing your CSV file '{file.name}'... Please wait while i analyze the data!").send()
    
    df_horse = dh.read(file.path)
    
    return df_horse

async def handle_attachment(user_message: cl.Message) -> None:
    """
    Handles different types of file attachments from the user message.

    Identifies the file type and processes it accordingly, storing the result in the session.

    Args:
    ----------
    user_message : Message
        The message containing file attachments and user input.
    """
    pdf_files = [file for file in user_message.elements if file.mime == "application/pdf"]
    txt_files = [file for file in user_message.elements if file.mime == "text/plain"]
    docx_files = [file for file in user_message.elements if file.mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    py_files = [file for file in user_message.elements if file.name.endswith(".py")]
    image_files = [file for file in user_message.elements if file.mime.startswith("image/")]
    csv_files = [file for file in user_message.elements if file.mime == "text/csv"]

    if pdf_files:
        file = pdf_files[0]
        chain = await process_pdf(file=file)
        cl.user_session.set("chain", chain)

    elif txt_files:
        file = txt_files[0]
        chain = await process_txt(file=file)
        cl.user_session.set("chain", chain)

    elif docx_files:
        file = docx_files[0]
        chain = await process_word(file=file)
        cl.user_session.set("chain", chain)

    elif py_files:
        file = py_files[0]
        chain = await process_python(file=file)
        cl.user_session.set("chain", chain)
        
    elif image_files:
        file = image_files[0]
        chain = await process_img(file=file, user_message=user_message)
        cl.user_session.set("chain", chain)
        
    elif csv_files:
        file = csv_files[0]
        chain = await process_csv(file=file)
        cl.user_session.set("chain", chain)
        
        user_message = user_message.content.strip() 
        answer = chain.chat(user_message)   
        
        await cl.Message(content=answer).send()
            
async def handle_files_from_audio_message(elements: list, user_message: str) -> None:
    """
    Processes files attached to an audio message and generates a response.

    Checks the types of files attached to the incoming audio message 
    and processes them accordingly. 

    Parameters:
    ----------
    elements : list
        A list of file elements attached to the audio message.
    user_message : str
        The message sent by the user that will be included in the response.

    Workflow:
    --------
    1. Identify the types of files attached to the audio message.
    2. For each file type:
        - Process the first file found of that type.
        - Store the generated chain if applicable.
    """
    file_types = {
        "pdf": [file for file in elements if file.mime == "application/pdf"],
        "txt": [file for file in elements if file.mime == "text/plain"],
        "docx": [file for file in elements if file.mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"],
        "py": [file for file in elements if file.name.endswith(".py")],
        "image": [file for file in elements if file.mime.startswith("image/")],
        "csv": [file for file in elements if file.mime == "text/csv"]
    }
    
    for file_type, files in file_types.items():
        if files:
            file = files[0]
            try:
                if file_type == "pdf":
                    chain = await process_pdf(file=file) 
                    cl.user_session.set("chain", chain)

                elif file_type == "txt":
                    chain = await process_txt(file=file) 
                    cl.user_session.set("chain", chain)

                elif file_type == "docx":
                    chain = await process_word(file=file) 
                    cl.user_session.set("chain", chain)

                elif file_type == "py":
                    chain = await process_python(file=file) 
                    cl.user_session.set("chain", chain)

                elif file_type == "image":
                    chain = await process_img(file=file, user_message=user_message) 
                    cl.user_session.set("chain", chain)
                    await speak_async(answer=chain)

                elif file_type == "csv":
                    chain = await process_csv(file=file)  
                    cl.user_session.set("chain", chain) 
                    answer = chain.chat(user_message)
                    
                    await cl.Message(content=answer).send()
                
            except Exception as e:
                
                print(f"Error during the {file.name} processing: {e}")
                
                continue 
