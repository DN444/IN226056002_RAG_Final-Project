from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from app.config import EMBEDDING_MODEL


def load_and_index(pdf_path="data/knowledge_base.pdf"):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(docs)

    vectordb = Chroma.from_documents(
        chunks,
        EMBEDDING_MODEL,
        persist_directory="./chroma_db"
    )

    return vectordb, chunks