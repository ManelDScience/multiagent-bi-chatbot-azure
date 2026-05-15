from pathlib import Path
from openai import OpenAI

from config import (
    FOUNDRY_OPENAI_ENDPOINT,
    FOUNDRY_OPENAI_KEY,
    FOUNDRY_OPENAI_DEPLOYMENT,
)


def load_prompt() -> str:
    prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "sql_agent.md"
    return prompt_path.read_text(encoding="utf-8")


def run_sql_agent(
    user_question: str,
    planner_output: str,
    schema_available: bool = False,
    schema_context: str = "",
    semantic_context: str = "",
) -> str:
    client = OpenAI(
        base_url=FOUNDRY_OPENAI_ENDPOINT,
        api_key=FOUNDRY_OPENAI_KEY,
    )

    system_prompt = load_prompt()

    schema_status = "SÍ" if schema_available else "NO"

    user_message = f"""
Estado del esquema: {"disponible" if schema_available else "no disponible"}

Información de esquema:
{schema_context if schema_context else "No se ha proporcionado información real del esquema."}

Pregunta original:
{user_question}

Contexto semántico:
{semantic_context if semantic_context else "No se ha proporcionado contexto semántico."}

Plan recibido:
{planner_output}

Prepara la respuesta del SQL Agent usando el formato indicado.
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