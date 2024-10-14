import chainlit as cl

async def select_chat_profile() -> list[cl.ChatProfile]:
    """
    Returns a list of available chat profiles for the user.

    Each profile includes a name, description, and associated icon.

    Returns:
        list: A list of chat profile objects.
    """
    return [
        cl.ChatProfile(
            name="LLaMa-3.1",
            markdown_description="The selected LLM model is **LLaMa-3.1**.",
            icon="https://1000logos.net/wp-content/uploads/2021/10/Meta-Symbol.png",
        ),
        cl.ChatProfile(
            name="LLaMa-3.2",
            markdown_description="The selected LLM model is **LLaMa-3.2**.",
            icon="https://1000logos.net/wp-content/uploads/2021/10/Meta-Symbol.png",
        ),
        
        cl.ChatProfile(
            name="LLaVa/LLaMa-3",
            markdown_description="The selected LLM model is **LLaVa/LLaMa-3**.",
            icon="https://llava-vl.github.io/llava-interactive/images/llava_interactive_logo.png",
        ),
        
        cl.ChatProfile(
            name="CodeOLLama",
            markdown_description="The selected LLM model is **CodeOLLama**.",
            icon="https://codellama.dev/icons/black-transparentbg.png",
        ),
        
        cl.ChatProfile(
            name="MistralNemo-12b",
            markdown_description="The selected LLM model is **Mistral-7b**.",
            icon="https://seeklogo.com/images/M/mistral-ai-icon-logo-B3319DCA6B-seeklogo.com.png",
        ),
        
        cl.ChatProfile(
            name="Gemma-2",
            markdown_description="The selected LLM model is **Gemma-2**.",
            icon="https://static.vecteezy.com/system/resources/previews/022/613/027/original/google-icon-logo-symbol-free-png.png",
        ),
                
        cl.ChatProfile(
            name="Qwen2.5-7b",
            markdown_description="The selected LLM model is **Qwen2.5-7b**.",
            icon="https://cdn.icon-icons.com/icons2/2232/PNG/512/alibaba_logo_icon_134594.png",
        ),
        
        cl.ChatProfile(
            name="Phi-3.5",
            markdown_description="The selected LLM model is **Phi-3.5**.",
            icon="https://static.vecteezy.com/system/resources/previews/027/127/473/non_2x/microsoft-logo-microsoft-icon-transparent-free-png.png",
        ),
    ]

async def initialize_chat_profile(chat_profile: str) -> str:
    """
    Sets up the chat profile based on user selection.

    Initializes the LLM and memory for the chat session 
    according to the selected profile.

    Args:
        chat_profile (str): The name of the selected chat profile.

    Returns:
        model_name: The name of the selected LLM in the chat_profile.
    """
    print(f'\nYou decided to use the LLM: {chat_profile}')
    
    model_mapping = {
        'LLaMa-3.1': 'llama3.1',
        'LLaMa-3.2': 'llama3.2',
        'LLaVa/LLaMa-3': 'llava-llama3',
        'CodeOLLama': 'codellama:7b',
        'MistralNemo-12b': 'mistral-nemo',
        'Gemma-2': 'gemma2',
        'Qwen2.5-7b':'qwen2.5:7b',
        'Phi-3.5': 'phi3.5'
    }
    
    if chat_profile in model_mapping:
        model_name = model_mapping[chat_profile]
        
        return model_name
