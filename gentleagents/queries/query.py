def get_agent_summary(chat_history):
    return (
        "Based on the conversation so far and the actions taken (including the tool outputs below),"
        " please provide what steps you took, which tools you used, and include a polite, short, concise general answer"
        " IF my query contains something that wasn't processed by the tools..\n\n"
        f"Conversation history:\n{chat_history}\n\n"
        "Final answer:"
    )

def get_team_system(lead_agent_name):
    return (
        f"You are {lead_agent_name}, the lead agent. Your job is to distribute tasks among specialized agents.\n\n"
        "You do not judge the responses by the agents, nor do you suggest any changes to the tools. You are simply a messenger.\n"
        "Here are the available agents and their tools:\n"
)

def get_team_followup(chat_history, lead_agent_name):
    return (
        f"You are {lead_agent_name}, the lead agent in this task delegation.\n"
        "Based on the conversation so far and the outcomes of the executed tasks, determine if there is another task required.\n"
        "From the conversation history, make SURE all tasks have been done!\n"
        "Return a JSON response in the following format and NOTHING ELSE:\n"
        '{ "continue": <true/false>, "task": {"agent": "<Agent Name>", "task": "<Task Description>"} }\n'
        "If no further tasks are needed, set \"continue\" to false and return null for \"task\".\n\n"
        "Conversation history:\n"
        f"{chat_history}\n"
    )


def get_team_summary(task_prompt, all_agent_responses):
    return (
        "You are the lead agent in this task delegation.\n"
        "Provide a factual summary of the task executions without any commentary, suggestions, or judgment. For each task, list:\n"
        " - The task assigned.\n"
        " - The agent that executed the task.\n"
        " - The tool used.\n"
        " - The exact output returned by the tool.\n\n"
        "Return ONLY the facts in the exact format above.\n\n"
        f"Task Prompt: {task_prompt}\n\n"
        "Agent Responses:\n"
        "\n".join(all_agent_responses)
    )

def get_team_initial_task():
    return (
        "\nAnalyze the task prompt and decide which agent should handle the VERY FIRST task.\n"
        "Return a JSON response with this format and NOTHING ELSE:\n"
        '{ "task": {"agent": "<Agent Name>", "task": "<Task Description>"} }'
    )
