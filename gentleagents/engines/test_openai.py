from gentleagents.engines.openai_client import interact

response = interact(
    system_prompt="You are a helpful assistant.",
    user_message="What is the capital of France?"
)

print(response)