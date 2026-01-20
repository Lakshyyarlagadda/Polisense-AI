import os

# ----------------------------------
# Force stable networking (Groq fix)
# ----------------------------------
os.environ["NO_PROXY"] = "*"
os.environ["GROQ_FORCE_IPV4"] = "1"

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

import streamlit as st
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FakeEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader

from assistant import Assistant
from gui import AssistantGUI
from prompts import SYSTEM_PROMPT

# ----------------------------------
# Streamlit Config
# ----------------------------------
st.set_page_config(
    page_title="PoliSense AI - Intelligent Employee Policy Assistant", layout="wide"
)

# ----------------------------------
# Initialize Session State
# ----------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "pdf_file_uploaded" not in st.session_state:
    st.session_state.pdf_file_uploaded = False


# ----------------------------------
# Load PDF & Create Vector Store
# ----------------------------------
@st.cache_resource(show_spinner="Indexing policy documents...")
def load_vectorstore_from_path(pdf_path: str) -> Chroma:
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )
    chunks = splitter.split_documents(documents)

    embeddings = FakeEmbeddings(size=384)

    return Chroma.from_documents(chunks, embeddings)


@st.cache_resource(show_spinner="Indexing uploaded PDF...")
def load_vectorstore_from_file(_uploaded_file) -> Chroma:
    import tempfile

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(_uploaded_file.read())
        tmp_file_path = tmp_file.name

    try:
        loader = PyPDFLoader(tmp_file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
        )
        chunks = splitter.split_documents(documents)

        embeddings = FakeEmbeddings(size=384)

        return Chroma.from_documents(chunks, embeddings)
    finally:
        os.unlink(tmp_file_path)


# Load default vectorstore if none exists
if st.session_state.vectorstore is None:
    st.session_state.vectorstore = load_vectorstore_from_path(
        "data/umbrella_corp_policies.pdf"
    )

if "employee_data" not in st.session_state:
    st.session_state.employee_data = None

# ----------------------------------
# Sidebar Settings
# ----------------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    temperature = st.slider(
        "LLM Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.05,
        key="llm_temperature",
    )

# ----------------------------------
# Groq LLM (Updated with current temperature)
# ----------------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=temperature,
)

# ----------------------------------
# Initialize or Update Assistant
# ----------------------------------
if "assistant" not in st.session_state:
    assistant = Assistant(
        system_prompt=SYSTEM_PROMPT,
        llm=llm,
        message_history=st.session_state.messages,
        vector_store=st.session_state.vectorstore,
        employee_information=st.session_state.employee_data,
    )
    st.session_state.assistant = assistant
else:
    # Update LLM with current temperature
    st.session_state.assistant.llm = llm

# ----------------------------------
# Initialize GUI
# ----------------------------------
gui = AssistantGUI(st.session_state.assistant)

# ----------------------------------
# Render GUI
# ----------------------------------
gui.render()
