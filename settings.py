# settings.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure that the required environment variables are set
required_env_vars = [
    "OPENAI_API_KEY",
    "GPT_MODEL_NAME",
    "PINECONE_API_KEY",
    "PINECONE_ENV",
    "PINECONE_INDEX",
    "RERANK_MODEL_NAME",
    "SECONDARY_GPT_MODEL",
    "TRANSCRIPTION_MODEL_NAME"
]

for var in required_env_vars:
    if var not in os.environ:
        raise EnvironmentError(f"Environment variable {var} is not set.")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GPT_MODEL_NAME = os.environ.get("GPT_MODEL_NAME")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINECONE_ENV")
PINECONE_INDEX = os.environ.get("PINECONE_INDEX")
RERANK_MODEL_NAME = os.environ.get("RERANK_MODEL_NAME")
UAE_NAMESPACE = {'ct': ['"ct_CBCR",', '"ct_ESR",', 'ct-decree-laws', 'ct_cabinet_decisions', 'ct_guides_Manuals',
                            'Double taxation_general'],
                     'vat': ['vat-cabinet-decisions', 'vat-decree-laws', 'vat-public-clarifications', 'vat-guides']
                     }
SECONDARY_GPT_MODEL = os.environ.get("SECONDARY_GPT_MODEL")
TRANSCRIPTION_MODEL_NAME = os.environ.get("TRANSCRIPTION_MODEL_NAME")
# Add any other settings you need to initialize here