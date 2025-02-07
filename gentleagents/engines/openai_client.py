import openai
import time

from gentleagents.loadenv.loadenv import OPENAI_API_KEY


MAX_RETRIES = 3  
RETRY_DELAY = 2  

def interact(system_prompt, user_message, tools=None, model="gpt-4-turbo"):
    """
    Sends a message to OpenAI's GPT model and returns the response.

    Args:
        system_prompt (str): The system-level instruction to guide the model.
        user_message (str): The user's input message.
        tools (list, optional): List of tool definitions for function calling.
        model (str, optional): OpenAI model to use (default is GPT-4-turbo).

    Returns:
        dict: The response from OpenAI API, or None if an error occurs.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set. Please configure your API key.")

    openai.api_key = OPENAI_API_KEY

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    params = {
        "model": model,
        "messages": messages,
    }

    if tools:
        params["tools"] = tools  
        params["tool_choice"] = "auto"

    client = openai.OpenAI()  

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(**params)
            return response  
        
        except openai.APIError as e:
            print(f"OpenAI API error (attempt {attempt}): {e}")
        except openai.RateLimitError as e:
            print(f"Rate limit exceeded (attempt {attempt}): {e}")
        except openai.OpenAIError as e:
            print(f"Unexpected OpenAI error (attempt {attempt}): {e}")
        except Exception as e:
            print(f"Unknown error (attempt {attempt}): {e}")

        if attempt < MAX_RETRIES:
            time.sleep(RETRY_DELAY)  

    print("Max retries reached. Failed to get a response.")
    return None  
