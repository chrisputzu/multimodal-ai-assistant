import chainlit as cl
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

async def create_chain_retriever(texts: str, source_prefix: str) -> ConversationalRetrievalChain:
    """
    Creates a conversational retrieval chain for processing texts.

    Splits the input texts, indexes them with embeddings, and prepares a conversational retrieval chain 
    that can retrieve relevant information while maintaining conversation context.

    Args:
        texts (str): The input text or collection of texts to process.
        source_prefix (str): A prefix for generating metadata for each text chunk.

    Returns:
        ConversationalRetrievalChain: A configured retrieval chain for text-based interactions.
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=100)
    texts = text_splitter.split_text(texts)
    metadatas = [{"source": f"{source_prefix}-{i}"} for i in range(len(texts))]
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    docsearch = await cl.make_async(Chroma.from_texts)(texts, embeddings, metadatas=metadatas)
    message_history = ChatMessageHistory()
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True)
  
    chain = ConversationalRetrievalChain.from_llm(
        ChatOllama(model="llama3.1"),
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        memory=memory,
        output_key="answer",
        return_source_documents=False 
        )

    return chain