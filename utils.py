import os
import streamlit as st
from datetime import datetime
from streamlit.logger import get_logger

# Import ChatNVIDIA from langchain.chat_models.nvidia_ai_endpoints
from langchain_nvidia_ai_endpoints import ChatNVIDIA
# Import HuggingFaceEmbeddings from langchain.embeddings.huggingface
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
# Import StrOutputParser from langchain.schema
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate

logger = get_logger('Langchain-Chatbot')

# Decorator to enable chat history
def enable_chat_history(func):
    current_page = func.__qualname__
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = current_page
    if st.session_state["current_page"] != current_page:
        try:
            st.cache_resource.clear()
            del st.session_state["current_page"]
            del st.session_state["messages"]
        except Exception as e:
            print(f"Error clearing session state: {e}")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    def execute(*args, **kwargs):
        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

def choose_custom_nvidia_key():
    nvidia_api_key = st.sidebar.text_input(
        label="NVIDIA API Key",
        type="password",
        placeholder="nvapi-...",
        key="SELECTED_NVIDIA_API_KEY"
    )
    if not nvidia_api_key:
        st.error("Please add your NVIDIA API key to continue.")
        st.info("Obtain your key from this link: https://developer.nvidia.com/nvidia-ai-cloud-services")
        st.stop()

    # Replace with available NVIDIA models if any
    models = ["mistralai/mixtral-8x7b-instruct-v0.1"]
    model = st.sidebar.selectbox(
        label="Model",
        options=models,
        key="SELECTED_NVIDIA_MODEL"
    )
    return model, nvidia_api_key

def configure_llm():
    available_llms = [
        "mistralai/mixtral-8x7b-instruct-v0.1",
        "use your NVIDIA API key"
    ]
    llm_opt = st.sidebar.radio(
        label="LLM",
        options=available_llms,
        key="SELECTED_LLM"
    )

    if llm_opt == "mistralai/mixtral-8x7b-instruct-v0.1":
        nvidia_api_key = st.secrets.get("NVIDIA_API_KEY", "")
        if not nvidia_api_key:
            st.error("Please set your NVIDIA API key in Streamlit secrets or select 'use your NVIDIA API key' to enter it manually.")
            st.stop()
        llm = ChatNVIDIA(
            model="mistralai/mixtral-8x7b-instruct-v0.1",
            api_key=nvidia_api_key,
            temperature=0.7,
            max_tokens=1024
        )
    elif llm_opt == "use your NVIDIA API key":
        model, nvidia_api_key = choose_custom_nvidia_key()
        llm = ChatNVIDIA(
            model=model,
            api_key=nvidia_api_key,
            temperature=0.5,
            top_p=1,
            max_tokens=1024
        )
    else:
        st.error("Invalid LLM option selected.")
        st.stop()
    return llm

def print_qa(cls, question, answer):
    log_str = "\nUse case: {}\nQuestion: {}\nAnswer: {}\n" + "------" * 10
    logger.info(log_str.format(cls.__name__, question, answer))

@st.cache_resource
def configure_embedding_model():
    embedding_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    return embedding_model

def sync_st_session():
    for k, v in st.session_state.items():
        st.session_state[k] = v
