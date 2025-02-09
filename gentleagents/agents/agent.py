from gentleagents.engines.openai_client import interact
from gentleagents.validations.models import ToolResponse
from pydantic import ValidationError
from typing import Callable, Dict, Any, get_type_hints
import json
from gentleagents.agents.helper import get_function_parameters, format_final_response
from gentleagents.queries.query import get_agent_summary

class Agent:
    def __init__(self, name, role, tools=None, model = None):
        """
        Initialize an AI Agent.

        Args:
            name (str): The agent's name.
            role (str): The agent's role (helps define its behavior).
            tools (list, optional): Functions the agent can use (default: None).
            model (str): The model to use as the engine
        """
        self.name = name
        self.role = role
        self.tools = tools or []
        self.model = model
        self.chat_history = []  

    def start_agent(self, user_message: str) -> str:
        try:
            self.chat_history.append({"role": "user", "content": user_message})

            tools_spec = []
            for name, func in self.tools.items():
                try:
                    tools_spec.append({
                        "type": "function",
                        "function": {
                            "name": name,
                            "description": func.__doc__ or "No description provided.",
                            "parameters": get_function_parameters(func)
                        }
                    })
                except Exception as e:
                    print(f"Error processing tool '{name}': {e}")
                    continue  

            try:
                response = interact(
                    system_prompt=f"You are {self.name}, a {self.role}.",
                    user_message=user_message,
                    tools=tools_spec,
                    model=self.model
                )
            except Exception as e:
                return f"Error communicating with AI model: {e}"

            message = response.choices[0].message
            self.chat_history.append({"role": "assistant", "content": message.content if message.content else ""})

            if not message.tool_calls:
                print(response.choices[0].message.content)
                return response.choices[0].message.content
                
            responses = []
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = tool_call.function.arguments

                if function_name not in self.tools:
                    responses.append(f"Error: Unknown tool '{function_name}'")
                    continue

                try:
                    if isinstance(function_args, str):
                        function_args = json.loads(function_args)

                    if not isinstance(function_args, dict):
                        raise TypeError(f"Expected dictionary for function arguments, got {type(function_args)}")

                    result = self.tools[function_name](**function_args)
                    type_hints = get_type_hints(self.tools[function_name])
                    return_type = type_hints.get("return", type(None))
                    validated_response = ToolResponse[return_type](result=result, message="Task completed with tool successfully.")
                    responses.append(f"Tool '{function_name}' executed successfully: {validated_response}")

                except ValidationError as e:
                    responses.append(f"Validation error in tool '{function_name}': {e}")
                except TypeError as e:
                    responses.append(f"Type error in tool '{function_name}': {e}")
                except Exception as e:
                    responses.append(f"Unexpected error during execution of '{function_name}': {e}")

            tool_responses = "\n".join(responses)
            self.chat_history.append({"role": "assistant", "content": tool_responses})

            summary_prompt = get_agent_summary(self.chat_history)

            try:
                final_response = interact(
                    system_prompt=f"You are {self.name}, a {self.role}.",
                    user_message=summary_prompt,
                    tools=None,
                    model=self.model
                )
            except Exception as e:
                return f"Error communicating with AI model for final response: {e}"

            final_message = final_response.choices[0].message.content
            self.chat_history.append({"role": "assistant", "content": final_message})

            print(f"{format_final_response(tool_responses)}\n\n{final_message}")
            return f"{format_final_response(tool_responses)}\n\n{final_message}"
        except Exception as e:
            return f"Critical error in agent execution: {e}"

