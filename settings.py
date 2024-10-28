# settings.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure that the required environment variables are set
required_env_vars = [
    "OPENAI_API_KEY",
    "SECONDARY_GPT_MODEL",
    "TRANSCRIPTION_MODEL_NAME"
]

for var in required_env_vars:
    if var not in os.environ:
        raise EnvironmentError(f"Environment variable {var} is not set.")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SECONDARY_GPT_MODEL = os.environ.get("SECONDARY_GPT_MODEL")
TRANSCRIPTION_MODEL_NAME = os.environ.get("TRANSCRIPTION_MODEL_NAME")
# Add any other settings you need to initialize here