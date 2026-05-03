from pathlib import Path
from openai import OpenAI

from config import (
    FOUNDRY_OPENAI_ENDPOINT,
    FOUNDRY_OPENAI_KEY,
    FOUNDRY_OPENAI_DEPLOYMENT
)

def load_promt() -> str:
    promp_path = Path(__file__).resolve().parents[1] / "prompts" / "planner.md"
    return promp_path.read_text(encoding="utf-8")

def run_planner(user_questions: str) -> str:
    client = OpenAI(
        base_url = FOUNDRY_OPENAI_ENDPOINT,
        api_key=FOUNDRY_OPENAI_KEY
    )

    system_promt = load_promt()

    response = client.chat.completions.create(
        model=FOUNDRY_OPENAI_DEPLOYMENT,
        messages=[
            {
                "role":"system",
                "content":system_promt
            },
            {
                "role":"user",
                "content":user_questions
            },
        ]
    )

    return response.choices[0].message.content
