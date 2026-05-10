import json
import re
from src.mcp_client import list_views, get_columns


PREFERRED_SCHEMAS = ["agg", "fact", "dim"]


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9áéíóúñüÁÉÍÓÚÑÜ ]", " ", text).lower()


def tokenize(text: str) -> set[str]:
    return set(normalize_text(text).split())


def score_candidate(user_question: str, schema: str, table: str) -> int:
    question_tokens = tokenize(user_question)
    table_tokens = tokenize(table.replace("_", " "))

    score = 0

    # Coincidencia por palabras
    score += len(question_tokens.intersection(table_tokens)) * 10

    # Priorización básica por schema
    if schema == "agg":
        score += 5
    elif schema == "fact":
        score += 3
    elif schema == "dim":
        score += 1

    # Heurísticas de negocio básicas
    q = normalize_text(user_question)
    table_lower = table.lower()

    if "año" in q or "year" in q:
        if "year" in table_lower:
            score += 20

    if "mes" in q or "month" in q:
        if "month" in table_lower or "monthyear" in table_lower:
            score += 20

    if "cliente" in q or "customer" in q:
        if "customer" in table_lower:
            score += 20

    if "grupo" in q or "buying" in q:
        if "buying" in table_lower or "group" in table_lower:
            score += 20

    if "ventas" in q or "sales" in q:
        if "sales" in table_lower:
            score += 15

    return score


def select_best_candidate(user_question: str, views: list[dict]) -> tuple[dict, list[dict]]:
    candidates = []

    for view in views:
        schema = view.get("TABLE_SCHEMA")
        table = view.get("TABLE_NAME")

        if not schema or not table:
            continue

        if schema not in PREFERRED_SCHEMAS:
            continue

        score = score_candidate(user_question, schema, table)

        candidates.append({
            "schema": schema,
            "table": table,
            "score": score,
        })

    if not candidates:
        raise ValueError("No se encontraron vistas/tablas candidatas.")

    candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)

    return candidates[0], candidates


def select_schema_context(user_question: str) -> str:
    views_raw = list_views()
    views = json.loads(views_raw)

    best, candidates = select_best_candidate(user_question, views)

    columns_context = get_columns(best["schema"], best["table"])

    top_candidates = candidates[:5]

    candidates_text = "\n".join(
        [
            f"- {c['schema']}.{c['table']} → score {c['score']}"
            for c in top_candidates
        ]
    )

    return f"""
TABLA/VISTA SELECCIONADA:
{best["schema"]}.{best["table"]}

SCORE DE SELECCIÓN:
{best["score"]}

CANDIDATAS EVALUADAS:
{candidates_text}

COLUMNAS DISPONIBLES:
{columns_context}
"""