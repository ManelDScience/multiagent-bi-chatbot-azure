from pathlib import Path
from openai import OpenAI

from config import (
    FOUNDRY_OPENAI_ENDPOINT,
    FOUNDRY_OPENAI_KEY,
    FOUNDRY_OPENAI_DEPLOYMENT,
)


def load_prompt() -> str:
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "planner.md"
    return prompt_path.read_text(encoding="utf-8")


def run_planner(user_question: str, semantic_context: str = "") -> str:
    client = OpenAI(
        base_url=FOUNDRY_OPENAI_ENDPOINT,
        api_key=FOUNDRY_OPENAI_KEY,
    )

    system_prompt = load_prompt()

    user_message = f"""
Pregunta del usuario:
{user_question}

Contexto semántico disponible:
{semantic_context if semantic_context else "No se ha proporcionado contexto semántico."}

Genera el plan de análisis.
"""

    response = client.chat.completions.create(
        model=FOUNDRY_OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content
