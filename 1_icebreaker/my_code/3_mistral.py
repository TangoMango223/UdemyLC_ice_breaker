# IceBreaker Code

# Take a prompt and give it parameters

# Import Statement
import pprint
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from linkedin import scrape_linkedin_profile
from langchain_community.chat_models import ChatOllama

# How to use Ollama:
# 1) Install Ollama
# 2) Follow instructions to install via terminal.
# 3) Can talk to Ollama in the terminal
# 4) Make sure to install olama in your virtual env too


information = """
"""

# Summary Template
summary_template = """
Write me a short song about Pembroke Welsh Corgis.
"""

# Set up the template. Combines data from information passed in, along with template structure.
# Input variables needs to be a list
summary_prompt_template = PromptTemplate(input_variables= ["information"], template = summary_template)

# Contains input variables, which are the keys to populate. So it's information.
# Also it needs the template, before injecting to variables.

# Set up the LLM. Like a wrapper. Temperature = not creative at all.
# llm = ChatOpenAI(temperature= 0, model_name = "gpt-4o")

# Meta's Llama 3:
llm = ChatOllama(model = "llama3")

# Tie it together. Bind LLM with the summary template we made.
# For some reason the syntax is template|llm_model
chain = summary_prompt_template|llm

# Get Linkedin Info
linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/aviraj-garcha-b205381b5")


res = chain.invoke(input={"information": information})
pprint.pp(res)

# Your code will fail if you don't set up env variable, OPENAI_API_KEY

# When we use LangChain, set as environment variable and does the rest for you.