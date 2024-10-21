import streamlit as st
import os
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import time
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

os.environ["NVIDIA_API_KEY"] = os.getenv("NVIDIA_API_KEY")
llm = ChatNVIDIA(model_name="meta/llama3-70b-instruct")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def vector_embedding():
    if "vectors" not in st.session_state:
        st.session_state.embeddings = NVIDIAEmbeddings()
        st.session_state.loader = PyPDFDirectoryLoader("./novels")
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=50)
        st.session_state.final_documents = []
        for doc in st.session_state.docs:
            st.session_state.final_documents.extend(st.session_state.text_splitter.split_documents([doc]))
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

st.title("NVIDIA NIM DEMO")
prompt_template = ChatPromptTemplate.from_template(
    """ 
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question.
    <context>
    {context}
    <context>
    Questions: {input}
    """
)

prompt1 = st.text_input("Enter Your Question From Documents")

if st.button("Documents Embedding"):
    try:
        vector_embedding()
        st.write("Vector Store DB Is Ready")
    except requests.exceptions.ConnectionError as e:
        st.error(f"Connection error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if prompt1:
    try:
        if "vectors" not in st.session_state:
            st.error("Vectors not initialized. Please embed the documents first.")
        else:
            document_chain = create_stuff_documents_chain(llm, prompt_template)
            retriever = st.session_state.vectors.as_retriever()
            retrieval_chain = create_retrieval_chain(retriever, document_chain)
            start = time.process_time()
            response = retrieval_chain.invoke({'input': prompt1})
            print("Response time:", time.process_time() - start)
            st.write(response['answer'])

            with st.expander("Document Similarity Search"):
                for i, doc in enumerate(response["context"]):
                    st.write(doc.page_content)
                    st.write("--------------------------------")
    except requests.exceptions.ConnectionError as e:
        st.error(f"Connection error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")