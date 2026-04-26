import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Load embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# Initialize vector store
vectorstore = Chroma(
    persist_directory="./vectorstore",
    embedding_function=embeddings
)

def add_documents(texts: list[str]):
    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.create_documents(texts)
    vectorstore.add_documents(chunks)
    print(f"Added {len(chunks)} chunks!")

def search_documents(query: str, k: int = 3) -> str:
    # Find most relevant chunks
    results = vectorstore.similarity_search(query, k=k)
    context = "\n".join([doc.page_content for doc in results])
    return context