from dotenv import load_dotenv
import os

PROJECT_ROOT_DIR = os.getcwd()
BASE_DIR = f'{PROJECT_ROOT_DIR}'
ENV_PATH = os.path.join(BASE_DIR, 'gentleagents/env/.env.development')
load_dotenv(ENV_PATH)


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')