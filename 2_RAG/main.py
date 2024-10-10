# Import statements
import os

# LangChain Imports
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings # handle word embeddings
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


# Create OpenAI Embeddings
embeddings = OpenAIEmbeddings()
llm = ChatOpenAI()

query = "What is Pinecone in Machine Learning?"

# # Check the result without context provided..
# chain = PromptTemplate.from_template(template=query)|llm

# # Get result
# result = chain.invoke(input = {})

# # Print result:
# print(result)

# Ok so now the answer knows what it is, but back in 2022, ChatOpen Models did not know :P

# -------------------------------------------------------------
# -------------------------------------------------------------

# Method 1: Using Default, provided prompt templates on LangChain Site

# Step 1: Make Vector Store
vectorstore = PineconeVectorStore(
    index_name = os.environ["INDEX_NAME"], embedding= embeddings # use same embeddings you used
)

# Retrieve the information using LangChain
# https://smith.langchain.com/hub/langchain-ai/retrieval-qa-chat
# Templates are critical to provide clear instructions, and potential templates of input/output

# Combine docs
#  What does it do? Get list of documents, format them all into a prompt.
# Then it puts it together to pass to LLM
# It passes ALL documents so you should make sure it fits.
# "Stuff Chain" = take all document and stuff, hopefully fit from context window

# This prompt - answer only based on context below...
retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

# Stuffing Chain - get relevant documents
combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)

# Need to get from vector store
retrieval_chain = create_retrieval_chain(retriever = vectorstore.as_retriever(),
                                         combine_docs_chain = combine_docs_chain)

# Math - do a similarity search - rag prompt, and send all of this to the LLM

# What if we don't want to do stuffing strategy - i.e. summarize each document?
# Use another chain

# result = retrieval_chain.invoke(input={"input": query})

# print(result)


# -------------------------------------------------------------
# -------------------------------------------------------------

# Method 2: Custom Prompt Template versus default provided.
# You will need to hard-code the promptTemplate

# Instead of the retrieval chain...

my_template = """ Use the following pieces of context to answer the question at the end. If you do not know the answer, just say that you do not know the answer, do not try to make up an answer. Use three sentences maximum and keep the answer as concise as possible.
Always say "thanks for asking!" at the end of the answer.

{context}

Question: {question}

Helpful Answer:
"""

# Convert to prompt template
custom_rag_prompt = PromptTemplate.from_template(my_template)

# Format Docs - takes all the documents, joins them and format to single string.
def format_docs(docs):
    # Take in some documents, and join
    return "\n\n".join(doc.page_content for doc in docs)


# PassThrough Function = passes thru the inputs unchanged in your chain
# Do this method if you are creating your own custom structure for input, outputs, versus a provided template
rag_chain = (
    {"context": vectorstore.as_retriever()|format_docs, "question": RunnablePassthrough()}
    | custom_rag_prompt # bind the prompt
    | llm    # bind the LLM OpenAI-4o
)

# Invoke it.
# This Chain takes in the query.
# The Rag Chain includes Vector Store information.

# Takes query as input, one string
new_result = rag_chain.invoke(input = query)

print(new_result)
# Check rag_chain structure - print(rag_chain)

# 