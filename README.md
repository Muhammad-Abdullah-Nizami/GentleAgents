# GentleAgents

GentleAgents is a simple AI agent framework built as a **practice project** by **Muhammad Abdullah Nizami**. This is **not** a production-ready library but rather a minimal implementation to explore AI agent architectures.

## **Inspiration**
This project draws inspiration from various AI agent libraries, including:
- [smol-agents (Hugging Face)](https://huggingface.co/smol-agents)
- [phidata](https://github.com/phidatahq/phidata)
- [CrewAI](https://github.com/joaomdmoura/crewai)
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
    """Adds two numbers."""
    return a + b

def sub_numbers(a: int, b: int) -> int:
    """Subtracts two numbers."""
    return a - b

agent = Agent(
    name="Assistant",
    role="You are an assistant that performs tasks only with the tools provided.",
    tools={"add_numbers": add_numbers, "sub_numbers": sub_numbers},
    model="gpt-4-turbo"
)

response = agent.start_agent("Can you add 5 and 7? And also subtract 9 from 20?")
print(response)
```

## **Running Tests**
You can run the test script given above using:
```sh
python -m gentleagents.agents.test_agent
```
At the project root.

## **Acknowledgments**
Special thanks to **Laiba Batool** for contributing and helping with development.

## **License**
This project is open-source but intended for learning and experimentation. Feel free to explore and modify, but use proper frameworks for real-world applications.

---
🚀 *Built by Muhammad Abdullah Nizami as a learning project.*

