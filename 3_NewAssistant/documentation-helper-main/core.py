# Doing Rag Stuff

# Goal - Retrieve, Generate

# ---------- Import Statements ----------

import os

# This chain's purpose is for LangChain to retrieve docs from VectorStores
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever

from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings # handle word embeddings
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# LangSmith activation for tracing:
from langsmith import Client
from langsmith import traceable

# Need LangChain Hub - download dynamically augmentation prompts (templates) 
from langchain import hub
from langchain_openai import OpenAIEmbeddings

# Combine or stuffing chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Load environment:
from dotenv import load_dotenv

# Load the .env file
load_dotenv()



# Take context from VecStore, combine/stuff, (Retrieve) then give to the LLM for generation

INDEX_NAME = "langchain-doc-index"

# --- Check Tracing on LangSmith ----
# client = Client(api_key=os.environ["LANGCHAIN_API_KEY"])



# ----------- Let's Begin! -----------

# STEP 1 - create the LLM call
def run_llm(query: str, chat_history):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    docsearch = PineconeVectorStore(index_name=INDEX_NAME, embedding=embeddings)
    chat = ChatOpenAI(verbose=True, temperature=0)

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    stuff_documents_chain = create_stuff_documents_chain(chat, retrieval_qa_chat_prompt)

    # The non-last retriever must be called as a function, .as_retriever()
    history_aware_retriever = create_history_aware_retriever(
        llm=chat, retriever=docsearch.as_retriever(), prompt=rephrase_prompt
    )
    
    # The last retreiver must be called as a method, not as a function.
    qa = create_retrieval_chain(
        retriever=history_aware_retriever, combine_docs_chain=stuff_documents_chain
    )

    # Invoke - make sure to pass chat_history.
    result = qa.invoke(input={"input": query, "chat_history": chat_history})
    # Create new dictionary - new mapping
    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"]
    }
    
    return new_result

# Common Mistake:
# Establish the LLM, embeddings, and docsearch (ref to PineCone)
# These 3 objects will tie together and needed for stuff_chain and create_retrieval_chain

# Step 2 - Call it
# if __name__ == "__main__":
#     res = run_llm(query = "What is LangChain?", chat_history)
#     print(res)
# for streamlit:
# Changing names:
# Under result, we have several keys...
# input -> query
# context -> source documents
# answer -> result
