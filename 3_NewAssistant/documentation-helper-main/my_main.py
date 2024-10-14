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

# Put at the top
# Set page config to wide mode and set a dark theme
st.set_page_config(layout="wide", page_title="LangChain Helper Bot", page_icon="🦜")

# Custom CSS to mimic LangChain's theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0B0F19;
        color: #E1E3E8;
    }
    /* Sidebar */
    .css-1d391kg {
        background-color: #171923;
    }
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #E1E3E8 !important;
    }
    /* Buttons */
    .stButton>button {
        background-color: #1A202C;
        color: #E1E3E8;
        border: 1px solid #2D3748;
    }
    /* Text input */
    .stTextInput>div>div>input {
        background-color: #1A202C;
        color: #E1E3E8;
        border: 1px solid #2D3748;
    }
    /* Highlight color */
    .highlight {
        color: #48BB78;
    }
</style>
""", unsafe_allow_html=True)

# Main content
st.title("🦜🔗 LangChain Helper Bot")

# Sidebar
with st.sidebar:
    st.title("User Profile")
    profile_pic = st.image("https://www.petfinder.com/sites/default/files/images/content/pembroke-welsh-corgi-detail-scaled.jpg", width=100)
    user_name = st.text_input("Name", value="John Doe")
    user_email = st.text_input("Email", value="john.doe@example.com")
    st.write(f"Welcome, {user_name}!")
    st.write(f"Email: {user_email}")

    if st.checkbox("Show experimental user info"):
        try:
            user_info = st.experimental_user
            st.write(f"Logged in as: {user_info.email}")
        except AttributeError:
            st.write("Experimental user info not available.")

# Initialize session state
if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Function to create sources string
def create_sources_string(source_urls) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "Sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string

# Main chat interface
prompt = st.text_input("Ask a question about LangChain:", placeholder="Enter your prompt here...")

if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(query=prompt, chat_history=st.session_state["chat_history"])
        sources = set(doc.metadata["source"] for doc in generated_response["source_documents"])
        formatted_response = f"{generated_response['result']}\n\n{create_sources_string(sources)}"
        
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))

# Display chat history
for idx, (user_query, generated_response) in enumerate(zip(st.session_state["user_prompt_history"], st.session_state["chat_answers_history"])):
    message(user_query, is_user=True, key=f"user_{idx}")
    message(generated_response, key=f"response_{idx}")

# Add LangChain logo or name at the bottom
st.markdown("<div style='text-align: center; color: #48BB78;'>Powered by LangChain</div>", unsafe_allow_html=True)

# Access secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]
