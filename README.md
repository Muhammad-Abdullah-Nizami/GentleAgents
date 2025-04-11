# GentleAgents

GentleAgents is a simple AI agents library built as a learning project by me to understand AI Agent workflows. This is **not** a production-ready library but rather a minimal implementation to explore AI agent architectures.

## **Inspiration**
This project draws inspiration from various AI agent libraries, including:
- [smol-agents (Hugging Face)](https://huggingface.co/docs/smolagents/en/index)
- [phidata](https://docs.phidata.com/)
- [CrewAI](https://www.crewai.com/)
- And other similar frameworks.

## **What This Is**
- A **barebones** implementation of AI agents that interact with tools.
- Focused on simplicity and **not intended for real-world production use**.
- Built using OpenAI's API to process messages and invoke tool functions, and Pydantic for validations.

## **What This Is Not**
- **Not production-ready**—use proper frameworks if deploying serious AI agents.
- **Not feature-rich**—it is minimal by design.

## **Installation**
Install using pip:
```
pip install gentleagents
```

## **Usage**

**(Recommended)** 
Here is a link to a notebook for your ease: https://colab.research.google.com/drive/13wQVAKotc1PXDr0MTnUxdanP8KBFtb8m#scrollTo=_BS8J5t-jPZK

Also given below is a short guide:

## **Place your API keys in a .env file**
Example .env file:
```python
OPENAI_API_KEY="OPENAI_KEY_IF_USING_OPENAI"
SENDER_EMAIL="OPTIONAL_FOR_EMAIL_EXAMPLE_TOOL"
SENDER_PASSWORD="OPTIONAL_FOR_EMAIL_EXAMPLE_TOOL"
GROQ_API_KEY="GROQ_KEY_IF_USING_GROQ"
GROQ_API_URL="https://api.groq.com/openai/v1"
```

## **Set up your "tools" (any Python functions)**
Make sure to include the function doc strings as that helps the Agent's performance
```python
from gentleagents import Agent, Team
import os
#Define your functions

#example tool 1
def add_numbers(a: int, b: int) -> int:
    """Use this function to add two numbers.
    
    Args:
        a: int: The first number
        b: int: The second number

    Returns:
        int: sum of a + b
    """
    return a + b

#example tool 2
def sub_numbers(a: int, b: int) -> int:
    """Use this function to subtract two numbers.
    
    Args:
        a: int: The first number
        b: int: The second number

    Returns:
        int: result of a - b
    """
    return a - b

#OPTIONAL Example tool

# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import smtplib

# def send_email(recipient: str, subject: str, content: str) -> str: 
#     """Use this function to send an email.

#     Args:
#         recipient:str: the recipients' email, comma seperated if multiple
#         subject:str: the email subject
#         content:str: the email body
#     """



#     #set your google smtp email and password here
#     SENDER_EMAIL=""
#     SENDER_PASSWORD=""




#     sender_email = SENDER_EMAIL
#     sender_password = SENDER_PASSWORD

#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = recipient
#     message["Subject"] = subject

#     message.attach(MIMEText(content, "plain"))

#     try:
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, recipient, message.as_string())
        
#         status = f"Successfully sent email to {recipient}"
#         return status
#     except Exception as e:
#         print(f"Error in Email tool: {str(e)}")
#         status = "Failed to send email."
#         return status
```

Then use them in your Agent/Team like so:

## **For Agent:**
```python

agent = Agent(name="Assistant",
            role="""You are an assistant that performs any tasks
            if they can be done by the tools provided to you. You make sure a task is done if a tool
            for it is available""",
            tools={"add_numbers": add_numbers,"sub_numbers": sub_numbers},
            model = "GROQ:llama-3.3-70b-versatile")
            # model = "GROQ:llama-3.3-70b-specdec")
            
            #If using OPENAI:
            # model = "OPENAI:gpt-4-turbo")

response = agent.start_agent("Can you add 5 and 7? And also subtract 9 from 20 thanks man, how are you btw?")

#prints the Agent's working by default, can also save the response in a variable for use
#print(response)

```

## **For Team:**

```python

add_agent = Agent(
    name="Addition Agent",
    role="Performs simple additions using the provided tool.",
    tools={"add_numbers": add_numbers},
    model="GROQ:llama-3.3-70b-versatile"
    #If using OPENAI:
    # model = "OPENAI:gpt-4-turbo")
)

sub_agent = Agent(
    name="Subtraction Agent",
    role="Performs simple subtractions using the provided tool.",
    tools={"sub_numbers": sub_numbers},
    model="GROQ:llama-3.3-70b-versatile"
    #If using OPENAI:
    # model = "OPENAI:gpt-4-turbo")
)

#optional agent if using the email tool
# email_agent = Agent(
#         name="Email Agent",
#         role="Sends emails using the provided tool.",
#         tools={"send_email": send_email},
#         model="GROQ:llama-3.3-70b-versatile"
#         #If using OPENAI:
#         # model = "OPENAI:gpt-4-turbo")
#     )

lead_agent = Agent(
    name="Lead Agent",
    role="Manages task delegation among specialized agents and summarizes results.",
    tools={},
    model="GROQ:llama-3.3-70b-versatile"
    #If using OPENAI:
    # model = "OPENAI:gpt-4-turbo")
)

team = Team(lead_agent, [add_agent, sub_agent])
tasks = "Add 5 and 3. and oh also subtract 4 from 10 thanks!"

result = team.assign_tasks(tasks)
print("\nFinal Team Output:\n", result)

#To test the email tool/Agent, uncomment below lines
# team_two = Team(lead_agent, [add_agent, sub_agent, email_agent])
# tasks = "Add 5 and 3. And email the answer to abdullah_nizami@live.com, and oh also subtract 4 from 10 thanks!"

# result_two = team_two.assign_tasks(tasks)
# print("\nFinal Team_two Output:\n", result)

```

## **License**
This project is open-source but intended for learning and experimentation. Feel free to explore and modify, but use proper frameworks for real-world applications.

---

🚀 *Built by Muhammad Abdullah Nizami as a learning project. Thanks for using :) To report any bugs, contribute to this project, or to collaborate on others, reach me at abdullah_nizami@live.com or abdullahnizami@iciltek.com or https://www.linkedin.com/in/muhammad-abdullah-nizami-318041237/*

