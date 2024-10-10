# -----------------
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


# -----------------
print("Initalizing VectorStore...")

# PDF Path:
pdf_path = "/Users/christine/VSCode/Udemy_LC_Icebreaker_1/UdemyLC_ice_breaker/2_RAG/Academic Prompting Guide.pdf"

# Load up document, read it and chunk PDF.
loader = PyPDFLoader(file_path = pdf_path)

# Has document, need to load it
documents = loader.load()

# It's ok to split for us, but we need to chunk it once more, to control it. Keep it mind it did for us.
text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 30, separator= "\n")

# Apply the splitter for documents
docs = text_splitter.split_documents(documents = documents)

# Apply OpenAI Embeddings (mapping):
embeddings = OpenAIEmbeddings()

# Call VectorStore and use FAISS
# You'll get an object in your computer representinng your vectorstore

# Set it up:
vectorstore = FAISS.from_documents(docs, embeddings)

# Save in RAM, otherwise it disappears:
vectorstore.save_local("faiss_index_react")

# Inspect store...
# vectorstore.similarity_search()
# You can see it is doing vector sim search for us

# Allow dangerous deserialization
# LangChain added this to address some safety issues
# Pickle File
# Security issues = accept for deserialization risk attacks
# Flag that this is acceptable


# Allow deserialization:
new_vectorstore = FAISS.load_local(
    "faiss_index_react", embeddings, allow_dangerous_deserialization= True
)

# We are using method 1 - custom LangSmith prompt template
retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

# Stuffer. Object is set up to 
combine_docs_chain = create_stuff_documents_chain(OpenAI(), retrieval_qa_chat_prompt)

# Now we have to put the chain together
retrieval_chain = create_retrieval_chain(new_vectorstore.as_retriever(), combine_docs_chain)

user_query= """ Give me a short summary about the main message for this PDF. """

# Put it together and invoke.
res = retrieval_chain.invoke({"input": user_query})
print(res)