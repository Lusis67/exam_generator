import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def build_vectorstore(content_folder="data/content", persist_directory="chroma_db"):
    docs = []
    for root, _, files in os.walk(content_folder):
        for filename in files:
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(os.path.join(root, filename))
                docs.extend(loader.load())
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(
        chunks, embeddings, persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb

def retrieve_relevant_chunks(query, k=5, persist_directory="chroma_db"):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    docs = vectordb.similarity_search(query, k=k)
    return "\n\n".join([doc.page_content for doc in docs])