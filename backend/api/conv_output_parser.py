from __future__ import annotations

from typing import Union

from langchain.agents import AgentOutputParser
from .Prompt import FORMAT_INSTRUCTIONS
from langchain.output_parsers.json import parse_json_markdown
from langchain.schema import AgentAction, AgentFinish, OutputParserException
import re
import json

def parse_json_markdown_with_code(json_string: str) -> dict:
    # Try to find JSON string within triple backticks
    match = re.search(r"```(json)?(.*?)```", json_string, re.DOTALL)

    # If no match found, assume the entire string is a JSON string
    if match is None:
        json_str = json_string
    else:
        # If match found, use the content within the backticks
        json_str = match.group(2)

        # Strip whitespace and newlines from the start and end
        json_str = json_str.strip()

        # Convert backticks portion to raw string
        # if "```" in json_string:
        #     json_str = f'r"""{json_str}"""'
        # Convert backticks portion to raw string
        if "```" in json_string:
            json_str = f'"{json_string[:match.start()]}{json_str}{json_string[match.end():]}"'

    # Parse the JSON string into a Python dictionary
    try:
        parsed = json.loads(json_str)
    except Exception as e:
        parsed = {"action": "Final Answer", "action_input": json_str}
        
        # if "action_input" in json_str:
        #     parsed["action_input"] = json_str.split("action_input")[1].split(":")[1]
        

    return parsed

class ConvoOutputParser(AgentOutputParser):
    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        try:
            response = parse_json_markdown(text)
            action, action_input = response["action"], response["action_input"]
            if action == "Final Answer":
                return AgentFinish({"output": action_input.strip()}, text)
            else:
                return AgentAction(action, action_input, text)
        except Exception as e:
            try:
                response = parse_json_markdown_with_code(text)
                action, action_input = response["action"], response["action_input"]
                if action == "Final Answer":
                    return AgentFinish({"output": action_input.strip()}, text)
                else:
                    return AgentAction(action, action_input, text)
            except Exception as e:
                raise OutputParserException(f"Could not parse LLM output: {text}") from e


    @property
    def _type(self) -> str:
        return "AI_Teaching_Assistant"
