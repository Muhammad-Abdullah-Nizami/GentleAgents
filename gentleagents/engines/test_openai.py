from gentleagents.engines.openai_client import interact

response = interact(
    system_prompt="You are a helpful assistant.",
    user_message="What is the capital of France?"
)

assistant_reply = response.choices[0].message.content

print(response)
print(assistant_reply)

#TO DO: REMOVE COMMENTS
#For Laiba:
#Run this file using python -m gentleagents.engines.test_openai at the project root.
#Root means at /GentleAgents