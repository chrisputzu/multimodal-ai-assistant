import asyncio
import concurrent.futures
from gtts import gTTS
from pathlib import Path
from pydub import AudioSegment
from pydub.playback import play

async def speak_async(answer: str) -> None:
    """
    Asynchronously converts text to speech in a separate thread.

    Uses a thread to handle the text-to-speech conversion without blocking the main event loop. 
    This approach is implemented to avoid the connection timeout issue in Chainlit, 
    which could result in losing the response.

    Args:
        answer (str): The text to convert into speech.

    Returns:
        None
    """
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        
        await loop.run_in_executor(pool, text_to_speech, answer)


def text_to_speech(answer: str) -> None:
    """
    Converts text to speech, saves it as an audio file, and plays the sound.

    Args:
        answer (str): The text to convert into speech.

    The audio is saved in the 'generated_audio' folder and played automatically.
    """
    try:
        tts = gTTS(text=answer, lang='en')
        audio_folder = Path("generated_audio")
        audio_folder.mkdir(exist_ok=True)
        audio_file = audio_folder / "output_audio.mp3"
        
        tts.save(str(audio_file))
        
        audio = AudioSegment.from_file(audio_file)
        play(audio)

    except Exception as e:
        print(f"An error occurred: {e}")






