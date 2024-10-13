# New Main File
# Streamlit - used to build front end

# core.py running function:
from core import run_llm

# Import Streamlit packages
import streamlit as st
from streamlit_chat import message # component of chat interface

# Time
import time

import uuid

# Generate a unique UUID

# streamlit run my_main.py
# Create a runner
# run main.py file.
# -----------------

# Start the code
st.header("LangChain🦜🔗 Udemy Course- Helper Bot")

# # Unique Key to handle duplications:
# unique_key = f"prompt_{uuid.uuid4()}"


# # Function to reset the input
# def reset_input():
#     st.session_state['user_input'] = ""

# Hold user input:
prompt = st.text_input("Prompt", placeholder="Enter your prompt here...")

# Initialize memory. We will be labelling them like this.
# We will be using two keys, chat answers and user answers.
# Clean state at the beginning.

# Initialize all states - required initalization for Streamlit and our application:
# Checks at the beginning when running a new streamlit application
if (
    "chat_answers_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state):
        st.session_state["chat_answers_history"] = []
        st.session_state["user_prompt_history"] = []
        st.session_state["chat_history"] = [] # This will hold both our history later.


# Define create_sources_string
def create_sources_string(source_urls) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string


if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(query=prompt)

        sources = set(doc.metadata["source"] for doc in generated_response["source_documents"])
        formatted_response = (
                f"{generated_response['result']} \n\n {create_sources_string(sources)}"
            )
        # print(generated_response["result"])
        # Insert session state   
            
        # We should write to it:
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        
        # Append together:
        st.session_state["chat_history"].append(("human", prompt)) # this is desired structure  
        st.session_state["chat_history"].append(("ai", generated_response["answer"])) # this is desired structure   
            

# Display the chat history
if st.session_state["chat_answers_history"]:
    for idx, (user_query, generated_response) in enumerate(zip(st.session_state["user_prompt_history"], st.session_state["chat_answers_history"])):
        message(user_query, is_user=True, key=f"user_{idx}")
        message(generated_response, key=f"response_{idx}")