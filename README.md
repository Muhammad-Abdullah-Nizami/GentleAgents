# GentleAgents

GentleAgents is a simple AI agent framework built as a **learning project** by **Muhammad Abdullah Nizami** to understand AI Agent workflows. This is **not** a production-ready library but rather a minimal implementation to explore AI agent architectures.

## **Inspiration**
This project draws inspiration from various AI agent libraries, including:
- [smol-agents (Hugging Face)](https://huggingface.co/docs/smolagents/en/index)
- [phidata](https://docs.phidata.com/)
- [CrewAI](https://www.crewai.com/)
- And other similar frameworks.

## **What This Is**
- A **barebones** implementation of AI agents that interact with tools.
- Built using **OpenAI's API** to process messages and invoke tool functions.
- Focused on simplicity and **not intended for real-world production use**.

## **What This Is Not**
- **Not production-ready**—use proper frameworks if deploying serious AI agents.
- **Not feature-rich**—it is minimal by design.

## **Installation**
You can clone the repository and install dependencies:
```sh
# Clone the repository
git clone https://github.com/yourusername/GentleAgents.git
cd GentleAgents

# Install dependencies
pip install -r requirements.txt
```

## **Usage**
Here’s an example of how to use **GentleAgents**:

```python
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

agent = Agent(
    name="Assistant",
    role="You are an assistant that performs tasks only with the tools provided.",
    tools={"add_numbers": add_numbers, "sub_numbers": sub_numbers},
    model = "OPENAI:gpt-4-turbo")

    #more examples below:
    #model = "GROQ:llama-3.3-70b-versatile")
    #model = "GROQ:llama-3.3-70b-specdec")

    #include provider then model
    #only OPENAI and GROQ supported for now
)

response = agent.start_agent("Can you add 5 and 7? And also subtract 9 from 20?")
print(response)
```
## **Place your API keys in the env folder in a .env.development file**
example .env.development file:
```python
OPENAI_API_KEY="OPENAI_KEY_IF_USING_OPENAI"
SENDER_EMAIL="OPTIONAL_FOR_EMAIL_EXAMPLE_TOOL"
SENDER_PASSWORD="OPTIONAL_FOR_EMAIL_EXAMPLE_TOOL"
GROQ_API_KEY="GROQ_KEY_IF_USING_GROQ"
GROQ_API_URL="https://api.groq.com/openai/v1"
```

## **Running Tests**
You can run the test script given above using:
```sh
python -m gentleagents.agents.test_agent
```
At the project root.

### Expected Response

```
Tool 'add_numbers' executed successfully: result=12 message='Task completed with tool successfully.'
Tool 'sub_numbers' executed successfully: result=11 message='Task completed with tool successfully.'
```

## **License**
This project is open-source but intended for learning and experimentation. Feel free to explore and modify, but use proper frameworks for real-world applications.

---
🚀 *Built by Muhammad Abdullah Nizami as a learning project.*

