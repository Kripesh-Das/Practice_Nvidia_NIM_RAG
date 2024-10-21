# NVIDIA NIM DEMO

This project demonstrates the use of NVIDIA's AI endpoints for document embedding and retrieval using Streamlit. The application allows users to embed documents from a directory and ask questions based on the embedded documents.

## Project Structure

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/nvidia-nim-demo.git
    cd nvidia-nim-demo
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory with the following content:

    ```properties
    NVIDIA_API_KEY = "your_nvidia_api_key"
    LANGCHAIN_TRACING_V2 = true
    LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY = "your_langchain_api_key"
    LANGCHAIN_PROJECT = "GenAIAppWithOpenAI"
    HF_TOKEN = "your_hf_token"
    ```

5. **Add your documents:**

    Place your PDF documents in the `novels/` directory.

## Running the Application

1. **Run the Streamlit application:**

    ```sh
    streamlit run final_app.py
    ```

2. **Open the application in your browser:**

    The application will be available at `http://localhost:8501`.

## Usage

1. **Embed Documents:**

    - Click the "Documents Embedding" button to embed the documents in the `novels/` directory.

2. **Ask Questions:**

    - Enter your question in the text input field and press Enter.
    - The application will retrieve the most relevant documents and provide an answer based on the embedded documents.

## Files

- **app.py:** Contains code to interact with OpenAI's API.
- **final_app.py:** Main Streamlit application file.
- **requirements.txt:** Lists the dependencies required for the project.
- **.env:** Environment variables for API keys and configurations.
