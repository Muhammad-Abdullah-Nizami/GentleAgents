from gentleagents.agents.agent import Agent

def add_numbers(a: int, b: int) -> int:
    """Adds two numbers and returns the result."""
    return a + b

def test_agent():
    agent = Agent(name="Assistant",
                role="""You are an assistant that doesn't perform any tasks if they cant
                be done by the tools provided to you.""",
                tools={"add_numbers": add_numbers},
                model = "gpt-4-turbo")

    response2 = agent.send_message("Can you add 5 and 7?")
    print(f"Function Call Response: {response2}")

test_agent()

#TO DO: REMOVE COMMENTS
#For Laiba
#Run this test using python -m gentleagents.agents.test_agent at the project root
#root is at /GentleAgent
