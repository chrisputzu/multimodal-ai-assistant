import pathlib
import torch
import asyncio
from diffusers import StableDiffusionPipeline

async def generate_image(user_message: str) -> str:
    """
    Generates an image based on the user's message using a stable diffusion model.

    Args:
        user_message (str): The message input from the user.

    Returns:
        str: The file path of the generated image saved as 'generated_image.png'.
    """    
    model_id = "CompVis/stable-diffusion-v1-4"
    
    if torch.cuda.is_available():
        pipe_model = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        pipe_model = pipe_model.to("cuda") 
    else:
        pipe_model = StableDiffusionPipeline.from_pretrained(model_id)

    generated_image = await asyncio.to_thread(pipe_model, user_message)
    generated_image = generated_image.images[0]

    generated_images_dir = pathlib.Path("generated_images")
    generated_images_dir.mkdir(exist_ok=True) 
    output_path = generated_images_dir / "generated_image.png"
    generated_image.save(output_path)
    string_path = str(output_path)

    return string_path