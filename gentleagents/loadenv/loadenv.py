from dotenv import load_dotenv
import os

DEFAULT_ENV_PATH = os.path.join(os.getcwd(), ".env")

ENV_PATH = os.getenv("GENTLEAGENTS_ENV_PATH", DEFAULT_ENV_PATH)

load_dotenv(ENV_PATH)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = os.getenv('GROQ_API_URL')
