![logo](public/logo_dark.png)

# Multimodal AI Assistant! 🚀🤖

The `Multimodal AI Assistant` is a free AI chatbot crafted to facilitate local interactions with various LLMs, documents, and a range of advanced functionalities. It leverages the `Chainlit` Framework, along with Agents and Chains, to enhance the user experience.

![Alt text](test_files_demo/chat_profiles_llm.png)

## Local LLMs 🔒

Harnessing models via `Langchain` and `ChatOllama`, hosted locally with `Ollama`, offers numerous benefits in terms of customization. This setup allows for tailored model configurations that align with specific project requirements, enabling developers to fine-tune performance and functionalities.

## Literalai storage and obstervability ☁️👁️

`Literalai` provides seamless integration for data storage and observability, ensuring efficient management and monitoring of your AI model's performance. With built-in support for handling large datasets and real-time analytics, Literalai allows you to track, store, and visualize key metrics, offering deep insights into your models' behavior and outcomes. This robust storage system simplifies debugging and optimizes performance, making it a crucial tool for developing scalable AI applications.

## Key Features 🌟

1. **Chat with Documents** 📄  

   Interact with various document formats, including `PDF`, `TXT`, `.PY`, `DOCX`, `images` and `CSV` files, using a `Retrieval Augmented Generation` (RAG) approach.

![alt text](test_files_demo/chat_pdf.png)
![alt text](test_files_demo/chat_image.png)
![alt text](test_files_demo/chat_csv.png)


2. **Speech to Text and Text to Speech** 🗣️  
   
   Utilize multimodal capabilities of `speech-to-text` and `text-to-speech` to interact with the assistant via both text and audio.

![Alt text](test_files_demo/voice_chat.png)

3. **Image Generation** 🖼️  
   
   Generate images locally using `StableDiffusion` with the **CompVis/stable-diffusion-v1-4** model, downloaded using the `diffusers` library.

![Alt text](test_files_demo/image_generation.png)

4. **Wikipedia Search** 🔍  
   
   Perform searches on `Wikipedia` by entering keywords after the first word of the command, which must be `Wikipedia` or `wikipedia`, to trigger the functionality.

![Alt text](test_files_demo/wikipedia_search.png)

5. **HTML Web Page Scraper** 🌐  
   
   Extract HTML code from a Web Page using `BeautifulSoup`.

![Alt text](test_files_demo/html_web_page_scraper.png)

6. **DuckDuckGo Web  Search** 🔎  
   
   Conduct searches directly on the `DuckDuckGo` browser, returning the first 10 search results.

![Alt text](test_files_demo/duckduckgo_web_search.png)

7. **Resume Chats** 💬🔄
   
   Users can effortlessly retrieve and continue previous chat sessions, ensuring a smooth conversation flow.

![alt text](test_files_demo/resume_chat.png)

8. **Literal Ai Storage anche chats** ☁️👁️
   
   Integration with Literal AI enables efficient cloud storage of chat histories, allowing quick access to past interactions.

![alt text](test_files_demo/literalai.png)
   
## Setup Instructions ⚙️

To get started, follow these simple steps:

1. **Clone the repository**  
   Run the following command to clone the repository:  
   ```bash 
   git clone https://github.com/chrisputzu/multimodal-ai-assistant.git
   ```
   Then navigate into the project directory:  
   ```bash
   cd multimodal-ai-assistant
   ```
2. **Install dependencies**  
   Install the required packages by running:  
   ```bash 
   pip install -r requirements.txt
   ```
3. **Download and Install Ollama**  
   Ollama is required for running models locally. Follow these instructions for your operating system:

   - **Windows/Linux/macOS**:  
   Visit the [Ollama Download Page](https://ollama.com/download) and follow the instructions to install Ollama on your machine.

4. **Download Local LLM**  
   
   After installing Ollama, you will need to download the models. Use the following commands:

   - For Llama3.1:  
     ```bash 
     ollama pull llama3.1

   - For Llama3.2:  
     ```bash
     ollama pull llama3.2

   - For LLava:  
     ```bash
     ollama pull llava-llama3

   - For CodeOLLama:  
     ```bash
     ollama pull codellama:7b

   - Per MistralNemo-12b:  
     ```bash
     ollama pull mistral-nemo

   - Per Gemma-2:  
     ```bash
     ollama pull gemma2

   - Per Qwen2.5-7b:  
     ```bash
     ollama pull qwen2.5:7b

   - Per Phi-3.5:  
     ```bash
     ollama pull phi3.5

5. **Literal**

   To create an account on [Literal AI](https://literalai.com/), visit the website and click on **Sign Up**. After confirming your email, log in to the dashboard and create a new project by clicking on **Create Project**. Finally, navigate to **Settings**, locate the **API Keys** section, and click on **Generate API Key** to obtain your API key.


6. **Configure your environment**   
   
   Set up your Chainlit API by running the following command in your terminal:  
   ```bash
   chainlit create-secret
   ```

   Create a `.env` file in the root directory and add your previously created API keys:  
   
   `CHAINLIT_API_KEY=<YOUR_CHAINLIT_API_KEY>` 

   `LITERAL_API_KEY=<YOUR_LITERAL_API_KEY>`

7.  **Run the application**  
    
      Start the assistant with:  

      ```python
      chainlit run app.py --port <YOUR_PORT>
      ```
      This will open the localhost page `localhost:<YOUR_PORT>`.

## Contact Information 📧

For inquiries, feel free to reach out via email:  
**Email:** [christian.putzu.job@gmail.com](mailto:christian.putzu.job@gmail.com)
