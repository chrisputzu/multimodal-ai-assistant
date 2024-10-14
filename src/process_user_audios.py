import chainlit as cl
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
from langchain_community.chat_models import ChatOllama
from src.create_chain_retrievers import create_chain_retriever
from src.process_user_files import handle_files_from_audio_message
from src.generate_images  import generate_image
from src.search_wikipedia_queries import search_wikipedia_query
from src.topic_classifier import classify_intent
from src.scrape_links import scrape_link
from src.search_duckduckgo_queries import agent_results_text
from src.process_text_to_speech import speak_async

async def process_audio_chunk(audio_chunk: cl.AudioChunk) -> BytesIO:
    """
    Handles incoming audio chunks and stores them in a buffer for further processing.

    Args:
        chunk (cl.AudioChunk): The audio data to process.

    Returns:
        BytesIO: The buffer containing the audio data.
    """
    if audio_chunk.isStart:
        buffer = BytesIO()
        buffer.name = f"input_audio.{audio_chunk.mimeType.split('/')[1]}"
        cl.user_session.set("audio_buffer", buffer)
        cl.user_session.set("audio_mime_type", audio_chunk.mimeType)

    audio_buffer = cl.user_session.get("audio_buffer")
    audio_buffer.write(audio_chunk.data)
    
    return audio_buffer

async def convert_audio_to_wav(audio_buffer: BytesIO, mime_type: str) -> BytesIO:
    """
    Converts audio data to WAV format.

    Args:
        audio_buffer (BytesIO): The buffer containing audio data.
        mime_type (str): The MIME type of the audio.

    Returns:
        BytesIO: The buffer containing the WAV audio data.
    """
    audio_buffer.seek(0)
    audio_segment = AudioSegment.from_file(audio_buffer, 
                                           format=mime_type.split('/')[1])
    buffer_wav = BytesIO()
    audio_segment.export(buffer_wav, format='wav')
    buffer_wav.seek(0)
    
    return buffer_wav

async def audio_answer(elements: list, model_name: str) -> None:
    """
    Transcribes audio input, processes the message, and generates a response.

    Args:
        elements (list): Additional elements like files or images that affect the response.
        model_name (str): The name of the language model used for generating responses.

    Returns:
        None
    """
    recognizer = sr.Recognizer()
    audio_buffer = cl.user_session.get("audio_buffer")
    audio_buffer.seek(0)
    mime_audio_message = cl.user_session.get("audio_mime_type")
    audio_wav = await convert_audio_to_wav(audio_buffer=audio_buffer, mime_type=mime_audio_message)

    try:
        with sr.AudioFile(audio_wav) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)  
            audio = recognizer.record(source)  
            transcription = recognizer.recognize_google(audio, language="en_EN")

        chain = await create_chain_retriever(texts=transcription, source_prefix="text/plain")
        
        await cl.Message(content=transcription, elements=elements).send()
        
        if elements:           
              
            for file in elements:
                
                if file.mime == "text/csv":
                    await handle_files_from_audio_message(elements=elements, user_message=transcription)
                
                elif file.mime.startswith("image/"):
                    await handle_files_from_audio_message(elements=elements, user_message=transcription)
                
                else: 
                    cb = await handle_files_from_audio_message(elements=elements, user_message=transcription) 
                    
                    response = await chain.ainvoke(transcription, callbacks=[cb])
                    answer = response["answer"]
                    
                    await cl.Message(content=answer).send()
                    await speak_async(answer=answer)
                       
        else:
            intent = await classify_intent(user_message=transcription)

            if 'image' in intent:
                print('Your intent is: ', intent)
                                
                await cl.Message(content="🖼️ Image Generation Selected! 🖼️ \n You've chosen to generate an image. Please note that if you don't have a GPU, the CUDA option won't be available, and it may take up to 15 minutes to generate a 512x512 image.").send()
                
                generated_image_path = await generate_image(user_message=transcription)
                image_element = cl.Image(name="Generated Image", path=str(generated_image_path))
                
                await cl.Message(content="✨ Here you go! ✨ \n Here’s the generated image!", elements=[image_element]).send()
            
            elif 'wikipedia' in intent:
                print('Your intent is: ', intent)
                
                query = transcription.split(' ')[1:]
                keywords_string = ''.join(query)
                
                await cl.Message(content="🔍 Wikipedia Search Selected! 🔍\n You've chosen to search on Wikipedia. Please enter your topic in the form of keywords below!").send()
                
                url, content = await search_wikipedia_query(user_message=keywords_string)
                formatted_results = f"🔗 **Source Link:** {url}\n\n📖 **Content:** {content}"
                
                await cl.Message(content=formatted_results).send()
            
            elif 'scraper' in intent:
                print('Your intent is: ', intent)
                
                scraped_link = await scrape_link(user_message=transcription)
                link_element = cl.File(name='Extracted link', path=scraped_link)
                
                await cl.Message(content='🎉 Your link has been successfully extracted 🎉.\n Click here to access the content directly!: ', elements=[link_element]).send()
 
            elif 'search' in intent:
                print('Your intent is: ', intent)
                                
                await cl.Message(content="🌐 DuckDuckGo Search Selected! 🌐 \n You've chosen to search on the DuckDuckGo Web Browser.\n The first 10 links will be displayed.").send()
                
                search_results = await agent_results_text(user_message=transcription)
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
                answer = await model.ainvoke(transcription)
                
                await cl.Message(content=answer.content).send()  
                await speak_async(answer=answer.content) 

    except sr.UnknownValueError:
        
        await cl.Message(content="Impossible to recognize the input audio message").send()



