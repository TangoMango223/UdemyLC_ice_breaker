# My Ingestion File - see ingestion.py for full solution

# Documentation file 
# Read the docs loader


# ----------
# Import statements
import os
from dotenv import load_dotenv

load_dotenv()

# LangChain Statements plus Vector Store
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

# Add Streamlit import
import streamlit as st


# Firecrawl
from firecrawl import FirecrawlApp

# Take index_name
# from consts import INDEX_NAME
from pinecone.grpc import PineconeGRPC as Pinecone

INDEX_NAME = "langchain-doc-index"

# Initialize embeddings - same as what you set in Vector Store
embeddings = OpenAIEmbeddings(model= "text-embedding-3-small")

# Function for ingestion
def ingest_docs():
    
    # Loader - includes the path
    loader = ReadTheDocsLoader("/Users/christine/VSCode/Udemy_LC_Icebreaker_1/UdemyLC_ice_breaker/3_NewAssistant/documentation-helper-main/langchain-docs/langchain.readthedocs.io/en/latest")
    
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


# ----- Ingestion with FireCrawler - ---

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import FireCrawlLoader

def ingest_docs2() -> None:
    langchain_documents_base_urls = [
        "https://python.langchain.com/v0.2/docs/integrations/chat/",
        "https://python.langchain.com/v0.2/docs/integrations/llms/",
        "https://python.langchain.com/v0.2/docs/integrations/text_embedding/",
        "https://python.langchain.com/v0.2/docs/integrations/document_loaders/",
        "https://python.langchain.com/v0.2/docs/integrations/document_transformers",
        "https://python.langchain.com/v0.2/docs/integrations/vectorstores/",
        "https://python.langchain.com/v0.2/docs/integrations/retrievers/",
        "https://python.langchain.com/v0.2/docs/integrations/tools/",
        "https://python.langchain.com/v0.2/docs/integrations/stores/",
        "https://python.langchain.com/v0.2/docs/integrations/llm_caching/",
        "https://python.langchain.com/v0.2/docs/integrations/graphs/",
        "https://python.langchain.com/v0.2/docs/integrations/memory/",
        "https://python.langchain.com/v0.2/docs/integrations/callbacks/",
        "https://python.langchain.com/v0.2/docs/concepts/",
    ]
    
    # Example case:
    langchain_documents_base_urls2 = [langchain_documents_base_urls[0]]
    
    all_docs = []
    for url in langchain_documents_base_urls2:
        print(f"FireCrawling {url=}")
        
        # Use WebBaseLoader instead of FireCrawlLoader
        loader = WebBaseLoader(url)
        
        docs = loader.load()
        print(f"Loaded {len(docs)} documents from {url}")
        all_docs.extend(docs)
        
    print(f"Total documents loaded: {len(all_docs)}")
    return all_docs
    
    # Uncomment these lines when you're ready to add to Pinecone
    # print(f"Going to add {len(all_docs)} documents to Pinecone")
    # PineconeVectorStore.from_documents(
    #     all_docs, embeddings, index_name="firecrawl-index"
    # )
    # print("****Loading to vectorstore done ***")

def ingest_docs3() -> None:
    langchain_documents_base_urls = [
        "https://python.langchain.com/v0.2/docs/integrations/chat/",
        "https://python.langchain.com/v0.2/docs/integrations/llms/",
        "https://python.langchain.com/v0.2/docs/integrations/text_embedding/",
        "https://python.langchain.com/v0.2/docs/integrations/document_loaders/",
        "https://python.langchain.com/v0.2/docs/integrations/document_transformers",
        "https://python.langchain.com/v0.2/docs/integrations/vectorstores/",
        "https://python.langchain.com/v0.2/docs/integrations/retrievers/",
        "https://python.langchain.com/v0.2/docs/integrations/tools/",
        "https://python.langchain.com/v0.2/docs/integrations/stores/",
        "https://python.langchain.com/v0.2/docs/integrations/llm_caching/",
        "https://python.langchain.com/v0.2/docs/integrations/graphs/",
        "https://python.langchain.com/v0.2/docs/integrations/memory/",
        "https://python.langchain.com/v0.2/docs/integrations/callbacks/",
        "https://python.langchain.com/v0.2/docs/concepts/",
    ]
    
    
    URL_TO_SCRAPE = "https://python.langchain.com/v0.2/docs/concepts/"
    
    api_token = os.environ["FIRECRAWL_API_KEY"]
    
    app = FirecrawlApp(api_key=api_token)
    
    scrape_status = app.scrape_url(
        URL_TO_SCRAPE,
        params = {
            "formats": ["markdown"],
            "onlyMainContent": True,
        }
    )
  
  
    print(scrape_status)
    
  
  
  
#    # all_docs = []
#     # # Crawl 1 to test:
#     # all_docs = langchain_documents_base_urls[0]
#     # for url in langchain_documents_base_urls:
#     #     print(f"FireCrawling {url=}")
#     #     loader = FireCrawlLoader(
#     #         url=url,
#     #         mode="crawl",
#     #         params={
#     #             "crawlerOptions": {"limit": 5},
#     #             "pageOptions": {"onlyMainContent": True},
#     #             "wait_until_done": True,
#     #         },
#     #     )
#     #     docs = loader.load()
#     #     print(f"Loaded {len(docs)} documents from {url}")
#     #     all_docs.extend(docs)
    
#     print(f"Total documents loaded: {len(all_docs)}")
#     return all_docs

# Uncomment these lines when you're ready to add to Pinecone
# print(f"Going to add {len(all_docs)} documents to Pinecone")
# PineconeVectorStore.from_documents(
#     all_docs, embeddings, index_name="firecrawl-index"
# )
# print("****Loading to vectorstore done ***")

# Add this import at the top of the file

# def ingest_docs4() -> None:
#     url = "https://python.langchain.com/v0.2/docs/integrations/chat/"
    
#     print(f"FireCrawling {url=}")
    
#     # Use FireCrawler directly
#     crawler = FireCrawler(
#         url=url,
#         mode="crawl",
#         limit=3,
#         max_depth=2,
#         ignore_robots_txt=False,
#         timeout=30000  # timeout in milliseconds
#     )
    
#     results = crawler.crawl()
    
#     print(f"Crawled {len(results)} pages")
    
#     for result in results:
#         print(f"URL: {result.url}")
#         print(f"Title: {result.title}")
#         print(f"Content length: {len(result.content)}")
#         print("---")
    
#     return results

# Call this:
if __name__ == "__main__":
    check_docs = ingest_docs3()
