from gentleagents.engines.openai_client import interact
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

    def send_message(self, user_message):
        """
        Sends a message to the agent and returns the response.
        Handles normal chat and function calling.

        Args:
            user_message (str): The user's input message.

        Returns:
            str: The agent's response or function call result.
        """
        self.chat_history.append({"role": "user", "content": user_message})

        tools_spec = [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": func.__doc__ or "No description provided.",
                    "parameters": {}  #TODO:
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
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name in self.tools:
                    result = self.tools[function_name](**function_args)
                    return f"Function '{function_name}' executed with {function_args}, result: {result}"

        return message.content

