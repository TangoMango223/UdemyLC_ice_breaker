# IceBreaker Code

# Take a prompt and give it parameters

# Import Statement
import pprint
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from linkedin import scrape_linkedin_profile


# information = """
# Christine Tang was born on some magic day in the 1990s, born in Canada.

# She is currently 27 years old and studying Artificial Intelligence at York University's Schulich School of Business.

# As she is strong in coding, she taught herself Python during the COVID-19 Pandemic back in 2020.
# """

# Summary Template
summary_template = """
Given the Linkedin information {information} about a person, I want you to create:
1. a short summary
2. two interesting facts about them.
3. suggested career paths for this individual.

Keep your summary no more than 30 words.
"""

# Set up the template. Combines data from information passed in, along with template structure.
# Input variables needs to be a list
summary_prompt_template = PromptTemplate(input_variables= ["information"], template = summary_template)

# Contains input variables, which are the keys to populate. So it's information.
# Also it needs the template, before injecting to variables.

# Set up the LLM. Like a wrapper. Temperature = not creative at all.
llm = ChatOpenAI(temperature= 0, model_name = "gpt-4o")

# Tie it together. Bind LLM with the summary template we made.
# For some reason the syntax is template|llm_model
chain = summary_prompt_template|llm

# Get Linkedin Info
linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/aviraj-garcha-b205381b5")


res = chain.invoke(input={"information": linkedin_data})
pprint.pp(res)

# Your code will fail if you don't set up env variable, OPENAI_API_KEY

# When we use LangChain, set as environment variable and does the rest for you.