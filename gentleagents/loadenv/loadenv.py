from dotenv import load_dotenv
import os

PROJECT_ROOT_DIR = os.getcwd()
BASE_DIR = f'{PROJECT_ROOT_DIR}'
ENV_PATH = os.path.join(BASE_DIR, 'gentleagents/env/.env.development')
load_dotenv(ENV_PATH)


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SENDER_EMAIL=os.getenv('SENDER_EMAIL')
SENDER_PASSWORD=os.getenv('SENDER_PASSWORD')
GROQ_API_KEY=os.getenv('GROQ_API_KEY')
GROQ_API_URL=os.getenv('GROQ_API_URL')