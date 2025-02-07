from gentleagents.engines.openai_client import interact
from gentleagents.validations.models import ToolResponse
from pydantic import ValidationError
from typing import Callable, Dict, Any, get_type_hints
import inspect
import json
class Agent:
    def __init__(self, name, role, tools=None, model="gpt-4-turbo"):
        """
        Initialize an AI Agent.

        Args:
            name (str): The agent's name.
            role (str): The agent's role (helps define its behavior).
            tools (list, optional): Functions the agent can use (default: None).
            model (str, optional): The model to use for chat (default: GPT-4-turbo).
        """
        self.name = name
        self.role = role
        self.tools = tools or []
        self.model = model
        self.chat_history = []  

    def start_agent(self, user_message: str) -> str:
        """Starts the agent, processes user input, and handles errors properly."""
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
                            "parameters": self.get_function_parameters(func)
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
            self.chat_history.append({"role": "assistant", "content": message.content})

            if not message.tool_calls:
                return message.content  

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

                    # Execute tool
                    result = self.tools[function_name](**function_args)
                    return_type = get_type_hints(self.tools[function_name])["return"]

                    validated_response = ToolResponse[return_type](result=result, message="Task completed with tool successfully.")
                    responses.append(f"Tool '{function_name}' executed successfully: {validated_response}")

                except ValidationError as e:
                    responses.append(f"Validation error in tool '{function_name}': {e}")
                except TypeError as e:
                    responses.append(f"Type error in tool '{function_name}': {e}")
                except Exception as e:
                    responses.append(f"Unexpected error during execution of '{function_name}': {e}")

            return "\n".join(responses)

        except Exception as e:
            return f"Critical error in agent execution: {e}"


    def python_type_to_json_schema(self, py_type: type) -> Dict[str, Any]:
        """Convert a Python type to a JSON Schema snippet."""
        try:
            mapping = {
                int: {"type": "integer"},
                float: {"type": "number"},
                str: {"type": "string"},
                bool: {"type": "boolean"},
            }

            if py_type in mapping:
                return mapping[py_type]

            print(f"Warning: Unsupported type '{py_type}'. Defaulting to 'string'.")
            return {"type": "string"}

        except Exception as e:
            print(f"Error converting Python type '{py_type}' to JSON Schema: {e}")
            return {"type": "string"}

    def get_function_parameters(self, func: Callable) -> Dict[str, Any]:
        """
        Extracts parameters from a function and returns a JSON Schema.

        Returns a schema like:
        {
            "type": "object",
            "properties": {
                "a": {"type": "integer"},
                "b": {"type": "integer"}
            },
            "required": ["a", "b"]
        }
        """
        try:
            signature = inspect.signature(func)
            properties = {}
            required = []

            for name, param in signature.parameters.items():
                try:
                    if param.annotation is inspect._empty:
                        json_type = {"type": "string"}
                    else:
                        json_type = self.python_type_to_json_schema(param.annotation)

                    properties[name] = json_type

                    if param.default is inspect._empty:
                        required.append(name)

                except Exception as e:
                    print(f"Error processing parameter '{name}' in function '{func.__name__}': {e}")
                    properties[name] = {"type": "string"}  

            schema = {"type": "object", "properties": properties}

            if required:
                schema["required"] = required

            return schema

        except Exception as e:
            print(f"Error extracting function signature for '{func}': {e}")
            return {"type": "object", "properties": {}} 
