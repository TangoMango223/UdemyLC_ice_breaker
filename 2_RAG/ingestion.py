#PineCone - Vector Store
import os
import dotenv

# LangChain Imports
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings # handle word embeddings
from langchain_pinecone import PineconeVectorStore


# Best Practice
# if __name__ == "__main__":
#     print("hello!")
    

# Medium file path:
file_path = "/Users/christine/VSCode/Udemy_LC_Icebreaker_1/UdemyLC_ice_breaker/2_RAG/rag-gist-setup/mediumblog1.txt"

# Put file of path:
loader = TextLoader(file_path)

# Load the file:
document = loader.load()
print("Loaded, now splitting...")

# If you check the object, it has stuff stored
# Meta Data important, gives you file path and other stuff

# Next part is text splitting:
# Rule: fit the context window (couple of chunks from the doc), and big enough, you would know what the chunk means
# Semantic meaning, we won't understand the LLM at all
# Rule of Thumb, use 1000
# Splitting Text to Chunk is important
# in LLM -> garbage in, garbage out.

# First, split characters
text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 0)

# Apply the split to document
text = text_splitter.split_documents(document)
print(f"Created {len(text)} chunks")

# Inside T_S -> used backslash n to do it, as separator

# Examine texts

# You should read the chunks and they should make sense.
# Read the content of the chunks and it should make sense - which it does.

# We may split bigger chunks
# Slightly larger chunks is OK here - 1000 chunks is not an issue.

# OpenAI Embedding objects
# Under the hood, use API and create a client
embeddings = OpenAIEmbeddings(openai_api_key = os.environ.get("OPENAI_API_KEY"))

print("ingesting...")

# Use PineCone - takes in the text (split from document into chunks), embeddings, index name
PineconeVectorStore.from_documents(text,embeddings, index_name = os.environ["INDEX_NAME"])

# LangChain will interact the chunks, embed them into the vector store, yay!
# You can write it on your own, but why would you lol.

# 