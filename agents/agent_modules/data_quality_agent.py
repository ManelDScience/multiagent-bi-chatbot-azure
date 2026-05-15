from pathlib import Path
from openai import OpenAI

from config import (
    FOUNDRY_OPENAI_ENDPOINT,
    FOUNDRY_OPENAI_KEY,
    FOUNDRY_OPENAI_DEPLOYMENT,
)


def load_prompt() -> str:
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "data_quality.md"
    return prompt_path.read_text(encoding="utf-8")


def run_data_quality_agent(
    user_question: str,
    query_result: str,
) -> str:
    client = OpenAI(
        base_url=FOUNDRY_OPENAI_ENDPOINT,
        api_key=FOUNDRY_OPENAI_KEY,
    )

    system_prompt = load_prompt()

    user_message = f"""
Pregunta original:
{user_question}

Resultado SQL:
{query_result}

Revisa la calidad básica del resultado antes de que lo use el Analyst Agent.
"""

    response = client.chat.completions.create(
        model=FOUNDRY_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )

    return response.choices[0].message.content