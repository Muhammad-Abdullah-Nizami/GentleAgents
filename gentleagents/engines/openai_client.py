import openai
import os
from gentleagents.loadenv.loadenv import OPENAI_API_KEY
def interact(system_prompt, user_message, tools=None, model="gpt-4-turbo"):
    """
    Sends a message to OpenAI's GPT model and returns the response.

    Args:
        system_prompt (str): The system-level instruction to guide the model.
        user_message (str): The user's input message.
        tools (list, optional): List of tool definitions for function calling.
        model (str, optional): OpenAI model to use (default is GPT-4-turbo).

    Returns:
        dict: The response from OpenAI API.
    """
    openai.api_key = OPENAI_API_KEY

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}]

    params = {
        "model": model,
        "messages": messages,
    }

    if tools:
        params["tools"] = tools  
        params["tool_choice"] = "auto"

    client = openai.OpenAI() 
    response = client.chat.completions.create(**params)
    return response