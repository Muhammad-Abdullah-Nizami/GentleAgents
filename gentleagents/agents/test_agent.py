from gentleagents.agents.agent import Agent
from gentleagents.tools.tool import add_numbers, sub_numbers, send_email
def test_agent():
    agent = Agent(name="Assistant",
                role="""You are an assistant that doesn't perform any tasks if they cant
                be done by the tools provided to you.""",
                tools={"add_numbers": add_numbers,"sub_numbers": sub_numbers, "send_email":send_email},
                model = "llama-3.3-70b-versatile")
    
    response = agent.start_agent("Can you add 5 and 7? And also subtract 9 from 20 thanks man, how are you btw?")
    # response = agent.start_agent("how are you btw?")
    # response = agent.start_agent("Can you subtract 5 from 7?")
    # response = agent.start_agent("Can you add 5 and 7? And also subtract 9 from 20 thanks man also email hi to abdullah_nizami@live.com")

    print(response)

test_agent()

#TO DO: REMOVE COMMENTS, ADD PROPER HANDLING FOR WHEN WE CHANGE ENGINES.
#For Laiba
#Run this test using python -m gentleagents.agents.test_agent at the project root
#root is at /GentleAgent
