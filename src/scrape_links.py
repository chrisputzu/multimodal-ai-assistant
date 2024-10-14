from pathlib import Path
import requests
from bs4 import BeautifulSoup
import html2text

async def scrape_link(user_message: str) -> str:
    """
    Scrapes html from a URL eb Page, converts it to Markdown format 
        and saves it in a .txt file.

    Args:
        user_message (str): The URL to scrape.

    Returns:
        str: Path to the text file containing the extracted Markdown content.
    """
    response = requests.get(user_message)
    soup = BeautifulSoup(response.content, "html.parser")
    
    html_content = soup.prettify()

    markdown_converter = html2text.HTML2Text()
    markdown_converter.ignore_links = False
    text_content = markdown_converter.handle(html_content)

    output_dir = Path("extracted_data")
    output_dir.mkdir(exist_ok=True)

    txt_file_path = output_dir / "extracted_link.txt"
    with txt_file_path.open(mode="w", encoding="utf-8") as txt_file:
        txt_file.write(text_content)
        
    file_path = str(txt_file_path)

    return file_path


