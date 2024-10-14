from typing import Union, List

from dotenv import load_dotenv
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool, tool
from langchain.tools.render import render_text_description
from langchain.agents.format_scratchpad.log import format_log_to_str


load_dotenv()


# -----------------

@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip(
        '"'
    )  # stripping away non alphabetic characters just in case

    return len(text)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")


if __name__ == "__main__":
    print("Hello ReAct LangChain!")
    print("----")
    tools = [get_text_length]

    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}
    
    Use the following format:
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin! Remember to always use the exact format specified above.
    
    Question: {input}
    Thought: {agent_scratchpad} 
    """
    # Agent_Scratchpad = the history of the conversation   

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    llm = ChatOpenAI(temperature=0, stop= ["\nObservation", "Observation"])
    
    # Create this variable to hold all the steps taken / history:
    intermediate_steps = []
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
            # format_log_to_str -> converts long logs from LLM actions to string
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser() # Structure the response in a way to understand, into structured data like Agent Action, Agent FInish.
        # If you run into an error, the best way to solve is to fix the input OR the prompt.
    )

# ---------------- Actual Implementation of REACT Model ---------------- 

    # THINKING of REACT - LLM going thru the steps and then describing =/= action
    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        {
            "input": "What is the length of 'DOG' in characters?",
            "agent_scratchpad": intermediate_steps,
        }
    )
    print("Thinking Stage:")
    print(agent_step)
    print("-----")
    print("Action Stage:")

    # ACTION STEP of REACT
    if isinstance(agent_step, AgentAction):
    # Get tool name it decided:
        tool_name = agent_step.tool
        # Retrieve actual tool object
        tool_to_use = find_tool_by_name(tools, tool_name)
        # Get what the tool input is taking
        tool_input = agent_step.tool_input
        observation = tool_to_use.func(str(tool_input))
        # OBSERVATION step
        print(f"{observation=}")
        
        # After everything, hold more history - agent step done, and observation.
        intermediate_steps.append((agent_step, str(observation)))
        print("-----")
        print("Intermediate Steps:")
        print(intermediate_steps)
        print("-----")
# -----------------
    # Let's do this again, continue the conversation.
    # LAST STEP - MOVE TO CONCLUSION - ANSWER. Notice that the LLM determined this agent step as "Finish".
    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        {
            "input": "What is the length of 'DOG' in characters?",
            "agent_scratchpad": intermediate_steps,
        })
    
    if isinstance(agent_step, AgentFinish):
        print("Agent Finish Actions:")
        print(agent_step.return_values)