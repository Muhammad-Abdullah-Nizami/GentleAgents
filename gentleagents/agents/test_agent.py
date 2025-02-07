from gentleagents.agents.agent import Agent
from gentleagents.tools.tool import add_numbers, sub_numbers, send_email
def test_agent():
    agent = Agent(name="Assistant",
                role="""You are an assistant that performs any tasks 
                if they can be done by the tools provided to you. You make sure a task is done if a tool
                for it is available""",
                tools={"add_numbers": add_numbers,"sub_numbers": sub_numbers, "send_email":send_email},
                model = "GROQ:llama-3.3-70b-versatile")
                # model = "GROQ:llama-3.3-70b-specdec")
                # model = "OPENAI:gpt-4-turbo")

    
    
    
    response = agent.start_agent("Can you add 5 and 7? And also subtract 9 from 20 thanks man, how are you btw?")
    # response = agent.start_agent("how are you btw?")
    # response = agent.start_agent("Can you subtract 5 from 7?")
    # response = agent.start_agent("Can you add 5 and 7? And also subtract 9 from 20 thanks man also email hi to abdullah_nizami@live.com")

    print(response)

test_agent()

#TO DO: REMOVE COMMENTS, ADD PROPER HANDLING FOR WHEN WE CHANGE ENGINES.
#Run this test using python -m gentleagents.agents.test_agent at the project root
#root is at /GentleAgent
