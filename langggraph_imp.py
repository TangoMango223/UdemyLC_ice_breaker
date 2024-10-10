# import os

# # LangChain Imports
# from langchain_community.document_loaders import TextLoader
# from langchain_text_splitters import CharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings # handle word embeddings
# from langchain_pinecone import PineconeVectorStore
# from langchain_core.prompts import PromptTemplate
# from langchain_openai import ChatOpenAI

# # LangGraph Imports
# from langgraph.graph import START, StateGraph
# from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# # Create OpenAI Embeddings
# embeddings = OpenAIEmbeddings()
# llm = ChatOpenAI()

# query = "What is Pinecone in Machine Learning?"

# # Step 1: Make Vector Store
# vectorstore = PineconeVectorStore(
#     index_name=os.environ["INDEX_NAME"], embedding=embeddings
# )

# # Prompt template for RAG (Retrieval-Augmented Generation)
# my_template = """Use the following pieces of context to answer the question at the end. If you do not know the answer, just say that you do not know the answer, do not try to make up an answer. Use three sentences maximum and keep the answer as concise as possible.
# Always say "thanks for asking!" at the end of the answer.

# {context}

# Question: {question}

# Helpful Answer:
# """

# # Convert to prompt template
# custom_rag_prompt = PromptTemplate.from_template(my_template)

# # Format Docs - takes documents and formats them into a single string
# def format_docs(docs):
#     return "\n\n".join(doc.page_content for doc in docs)

# # Initialize the StateGraph
# graph = StateGraph()

# # Adding steps to the graph (similar to defining nodes)
# # Step 1: Retrieve context using the vector store and format it
# graph.add(START, "Retrieve Context", vectorstore.as_retriever() | RunnableLambda(format_docs))

# # Step 2: Pass through the question
# graph.add(START, "Pass Question", RunnablePassthrough())

# # Step 3: Format the prompt with the context and question
# graph.add(["Retrieve Context", "Pass Question"], "Format Prompt", custom_rag_prompt)

# # Step 4: Process the formatted prompt with the LLM
# graph.add("Format Prompt", "LLM Processing", llm)

# # Input dictionary for running the graph
# input_data = {
#     "question": query
# }

# # Run the graph
# result = graph.run(input_data)

# # Print the result
# print(result)
