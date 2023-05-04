from dotenv import load_dotenv
from langchain.agents import Tool, AgentExecutor, LLMSingleActionAgent, AgentOutputParser, load_tools
from langchain.prompts import BaseChatPromptTemplate
from langchain import SerpAPIWrapper, LLMChain
from langchain.chat_models import ChatOpenAI
from typing import List, Union
from langchain.schema import AgentAction, AgentFinish, HumanMessage
from langchain.memory import ConversationBufferWindowMemory
import re
import asyncio
from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackManager
from langchain.callbacks.tracers import LangChainTracer
from aiohttp import ClientSession
import asyncio

load_dotenv(dotenv_path="../.env")

# Set up the base template
# Add this to the template for memory
# Previous conversation history:
# {history}

template = """"You are an AI Teaching Assistant. Answer the following questions as best as you can using your knowledge and expertise in the subject matter. You have access to the following tools:

{tools}

Use the following format:
Question: the input question you must answer
Thought: You should always think about what to do
Action: the action you take should be one of [{tool_names}] (optional)
Action Input: the input to the action (optional)
Observation: the result of the action (optional)
... (this Thought/Action/Action Input/Observation can repeat N times, if applicable)
Thought: I now know the final answer (optional)
Final Answer: ```a verbose final answer to the original input question which should be formatted in markdown format.```

Begin! Remember to be as authentic as possible as you are an AI Teaching Assistant! You may use the tools if necessary, but it is not mandatory.

Chat History:
{input}

{agent_scratchpad}
"""

# Setup template prompt

class CustomPromptTemplate(BaseChatPromptTemplate):
    # The template to use:
    template: str
    
    tools: List[Tool]
    
    def format_messages(self, **kwargs) -> str:
        # Get the intermediate steps (AgentAction, Observation tuples)
        # Format them in a particular way
        intermediate_steps = kwargs.pop("intermediate_steps")
        thoughts = ""
        for action, observation in intermediate_steps:
            thoughts += action.log
            thoughts += f"\nObservation: {observation}\nThought: "
        # Set the agent scratchpad variable to that value
        kwargs["agent_scratchpad"] = thoughts
        # Create a tools variable from the tools list
        kwargs["tools"] = "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])
        # Create a tool_names variable from the tools list
        kwargs["tool_names"] = ", ".join([tool.name for tool in self.tools])
        #kwargs["history"] = kwargs["history"].replace("\n", "\n\t")
        formatted = self.template.format(**kwargs)
        return [HumanMessage(content=formatted)]

# Output parser

class CustomOutputParser(AgentOutputParser):
    
    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:
        # Check if Agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output
            )
        # Parse out the action and action input
        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)
        if not match:
            # raise ValueError(f"Could not parse LLM output: `{llm_output}`")
            return AgentFinish(
                return_values={"output": llm_output},
                log=llm_output
            )
        action = match.group(1).strip()
        action_input = match.group(2)
        # return action and action input
        return AgentAction(
            tool=action,
            tool_input=action_input.strip(" ").strip('"'),
            log=llm_output
        )

output_parser = CustomOutputParser()

manager = BaseCallbackManager([StdOutCallbackHandler()])
llm = ChatOpenAI(temperature=0, callback_manager=manager)
async_tools = load_tools(["serpapi", "pal-math", "llm-math", "wolfram-alpha"], llm=llm, callback_manager=manager)
tool_names = [tool.name for tool in async_tools]
custom_prompt = CustomPromptTemplate(
    template=template,
    tools=async_tools,
    # This omits the `agent_scratchpad`, `tools`, and `tool_names` variables because those are generated dynamically
    # This includes the `intermediate_steps` variable because that is needed
    #input_variables=["input", "intermediate_steps", "history"], # Use when with history
    input_variables=["input", "intermediate_steps"],
)
llm_chain = LLMChain(llm=llm, prompt=custom_prompt, callback_manager=manager)

async def async_agent_executor(inputs):
    
    agent = LLMSingleActionAgent(
        llm_chain=llm_chain,
        output_parser=output_parser,
        stop=["\nObservation:"],
        allowed_tools=tool_names,
        callback_manager=manager
    )
    agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=async_tools, verbose=False, callback_manager=manager)
    return await agent_executor.arun(inputs)
    
if __name__ == "__main__":
    query = input("Enter a query: ")
    asyncio.run(async_agent_executor(query))