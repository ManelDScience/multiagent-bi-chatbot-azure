import os
from dotenv import load_dotenv

load_dotenv()

FOUNDRY_OPENAI_DEPLOYMENT = os.getenv("FOUNDRY_OPENAI_DEPLOYMENT")
FOUNDRY_OPENAI_KEY = os.getenv("FOUNDRY_OPENAI_KEY")
FOUNDRY_OPENAI_ENDPOINT = os.getenv("FOUNDRY_OPENAI_ENDPOINT")

def get_model_config():
    return {
        "model": FOUNDRY_OPENAI_DEPLOYMENT,
        "api_key": FOUNDRY_OPENAI_KEY,
        "base_url": FOUNDRY_OPENAI_ENDPOINT,
        "api_type": "azure"
    }
