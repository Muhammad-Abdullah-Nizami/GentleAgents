from gentleagents.agents.agent import Agent

def add_numbers(a: int, b: int) -> int:
    """Use this function to add two numbers.
    
    Args:
        a: int: The first number
        b: int: The second number

    Returns:
        int: sum of a + b
    """
    return a + b

def sub_numbers(a: int, b: int) -> int:
    """Use this function to subtract two numbers.
    
    Args:
        a: int: The first number
        b: int: The second number

    Returns:
        int: result of a - b
    """
    return a - b

def test_agent():
    agent = Agent(name="Assistant",
                role="""You are an assistant that doesn't perform any tasks if they cant
                be done by the tools provided to you.""",
                tools={"add_numbers": add_numbers, "sub_numbers": sub_numbers},
                model = "gpt-4-turbo")

    response2 = agent.start_agent("Can you add 5 and 7? And also subtract 9 from 20")
    # print(f"Function Call Response: {response2}")
    print(response2)

test_agent()

#TO DO: REMOVE COMMENTS
#For Laiba
#Run this test using python -m gentleagents.agents.test_agent at the project root
#root is at /GentleAgent
