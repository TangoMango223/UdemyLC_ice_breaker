# My Ingestion File - see ingestion.py for full solution

# Documentation file 
# Read the docs loader


# ----------
# Import statements
import os

# from dotenv import load_dotenv

# load_dotenv()

# LangChain Statements plus Vector Store
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Take index_name
# from consts import INDEX_NAME
from pinecone.grpc import PineconeGRPC as Pinecone

INDEX_NAME = "langchain-doc-index"

# ----------

# Initialize embeddings - same as what you set in Vector Store
embeddings = OpenAIEmbeddings(model= "text-embedding-3-small")

# Function for ingestion
def ingest_docs():
    
    # Loader - includes the path
    loader = ReadTheDocsLoader("/Users/christine/VSCode/Udemy_LC_Icebreaker_1/UdemyLC_ice_breaker/3_NewAssistant/api.python.langchain.com/en/latest")
    
    raw_documents = loader.load()
    
    # Print:
    print(f"loaded {len(raw_documents)} documents")
    
    # Text splitter:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)
    
    # Look in the documents
    for doc in documents:
        # Rename source for better searching, new URL
        # Indicate where the source came from
        # Take langchain-docs, and replace with https
        # Replace all mentions 
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        # Update URL
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} to Pinecone")
    
    # Put into PineCone:
    PineconeVectorStore.from_documents(documents, embeddings, index_name=INDEX_NAME)
    print("****Loading to vectorstore done ***")
    

# Mistake was made due to the way I configured my folder.
# I need to delete all the records in the Pinecone Store.



# def delete_all_entries():
#     # Initialize Pinecone with your API key and environment
#     pc = Pinecone(api_key=os.environ("PINECONE_API_KEY"), environment="us-east-1")
#     index = pc.Index(INDEX_NAME)

#     index.delete(delete_all=True, namespace='')






# Run these functions:

# Ingest documents
# ingest_docs()

# delete_all_entries()