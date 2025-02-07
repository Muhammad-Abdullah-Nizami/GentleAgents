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
        self.chat_history.append({"role": "user", "content": user_message})

        tools_spec = [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": func.__doc__ or "No description provided.",
                    "parameters": self.get_function_parameters(func)
                }
            }
            for name, func in self.tools.items()
        ]

        response = interact(
            system_prompt=f"You are {self.name}, a {self.role}.",
            user_message=user_message,
            tools=tools_spec,
            model=self.model
        )

        message = response.choices[0].message
        self.chat_history.append({"role": "assistant", "content": message.content})

        if message.tool_calls:
            responses = [] 

            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = tool_call.function.arguments

                #debugging purposes
                # print(f"Function name: {function_name}")
                # print(f"Function arguments: {function_args}")

                if function_name in self.tools:
                    try:
                        if isinstance(function_args, str):
                            function_args = json.loads(function_args)  

                        if not isinstance(function_args, dict):
                            raise TypeError(f"Expected dictionary for function arguments, but got {type(function_args)}")

                        result = self.tools[function_name](**function_args)
                        return_type = get_type_hints(self.tools[function_name])["return"]

                        validated_response = ToolResponse[return_type](result=result, message="Tool executed successfully.")
                        responses.append(f"Function '{function_name}' executed, result: {validated_response}")

                    except ValidationError as e:
                        responses.append(f"Validation error in tool '{function_name}': {e}")

                    except Exception as e:
                        responses.append(f"Error during tool execution for '{function_name}': {e}")

            return "\n".join(responses)


    def python_type_to_json_schema(self, py_type: type) -> Dict[str, Any]:
        """Convert a Python type to a JSON Schema snippet."""
        mapping = {
            int: {"type": "integer"},
            float: {"type": "number"},
            str: {"type": "string"},
            bool: {"type": "boolean"}
        }
        return mapping.get(py_type, {"type": "string"})

    def get_function_parameters(self, func: Callable) -> Dict[str, Any]:
        """
        Extract the parameters from a function and return a JSON Schema for them.
        
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
        signature = inspect.signature(func)
        properties = {}
        required = []
        for name, param in signature.parameters.items():
            if param.annotation is inspect._empty:
                json_type = {"type": "string"}
            else:
                json_type = self.python_type_to_json_schema(param.annotation)
            properties[name] = json_type
            if param.default is inspect._empty:
                required.append(name)
        schema = {
            "type": "object",
            "properties": properties
        }
        if required:
            schema["required"] = required
        return schema
