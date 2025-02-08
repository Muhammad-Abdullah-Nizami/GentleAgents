from gentleagents.agents.agent import Agent
from gentleagents.teams.team import Team
from gentleagents.tools.tool import add_numbers, sub_numbers, send_email

def test():
    add_agent = Agent(
        name="Addition Agent",
        role="Performs simple additions using the provided tool.",
        tools={"add_numbers": add_numbers},
        model="GROQ:llama-3.3-70b-versatile"
    )

    sub_agent = Agent(
        name="Subtraction Agent",
        role="Performs simple subtractions using the provided tool.",
        tools={"sub_numbers": sub_numbers},
        model="GROQ:llama-3.3-70b-versatile"
    )

    email_agent = Agent(
        name="Email Agent",
        role="Sends emails using the provided tool.",
        tools={"send_email": send_email},
        model="GROQ:llama-3.3-70b-versatile"
    )

    lead_agent = Agent(
        name="Lead Agent",
        role="Manages task delegation among specialized agents and summarizes results.",
        tools={},
        model="GROQ:llama-3.3-70b-versatile"
    )

    team = Team(lead_agent, [add_agent, sub_agent, email_agent])

    # tasks = "Add 5 and 3. And email the answer to abdullah_nizami@live.com, and oh also subtract 4 from 10 thanks!"
    tasks = "Add 5 and 3. and oh also subtract 4 from 10 thanks!"

    result = team.assign_tasks(tasks)

    print("\nFinal Team Output:\n", result)


test()
