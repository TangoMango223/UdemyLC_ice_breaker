# -------------------------------
# Import statements
import os

# LangChain Imports
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, OpenAI # handle word embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# New imports
from langchain import hub

# New imports for creating document chains + retrieval
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

# Runnable PassThrough - node connections with no ops
from langchain_core.runnables import RunnablePassthrough
# from langchain_community.document_loaders import PyPDFDirectoryLoader # READ PDFS
from langchain_community.document_loaders import PyPDFLoader

# Import FAISS - our local VectorStore
# From Facebook research - perform similarity searches
# Use Euclidean Distance - will fit into the ram
# Doesn't handle scalability, durability, etc.
# But for pure speed and simplicity, it's fully free, with LangChain
from langchain_community.vectorstores import FAISS

# -------------------------------

my_template = """ Use the following pieces of context to answer the question at the end. If you do not know the answer, just say that you do not know the answer, do not try to make up an answer. Use three sentences maximum and keep the answer as concise as possible.
Always say "thanks for asking!" at the end of the answer.

{context}

Question: {question}

Helpful Answer:
"""

# Work on this later