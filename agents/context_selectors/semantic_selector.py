import re


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9áéíóúñüÁÉÍÓÚÑÜ ]", " ", text).lower()


def extract_sections(semantic_context: str) -> list[dict]:
    sections = []
    current_title = None
    current_lines = []

    for line in semantic_context.splitlines():
        if line.startswith("## "):
            if current_title and current_lines:
                sections.append({
                    "title": current_title,
                    "content": "\n".join(current_lines).strip(),
                })

            current_title = line.replace("## ", "").strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_title and current_lines:
        sections.append({
            "title": current_title,
            "content": "\n".join(current_lines).strip(),
        })

    return sections


def score_section(user_question: str, section: dict) -> int:
    question = normalize_text(user_question)
    title = normalize_text(section["title"])
    content = normalize_text(section["content"])

    score = 0

    keywords = {
        "ventas": ["venta", "ventas", "sales", "importe"],
        "cliente": ["cliente", "clientes", "customer"],
        "tiempo": ["año", "mes", "trimestre", "fecha", "year", "month", "quarter", "date"],
        "producto": ["producto", "productos", "category", "categoría"],
        "reglas": ["regla", "excluir", "incluir", "criterio", "definición"],
    }

    for keyword_group in keywords.values():
        if any(word in question for word in keyword_group):
            if any(word in title for word in keyword_group):
                score += 10
            if any(word in content for word in keyword_group):
                score += 5

    # Bonus general si la sección habla de métricas y la pregunta parece pedir una métrica
    if any(word in question for word in ["ventas", "total", "importe", "sales"]):
        if "métrica" in title or "metric" in title:
            score += 10

    # Bonus general si la pregunta usa dimensiones temporales
    if any(word in question for word in ["año", "mes", "trimestre", "fecha"]):
        if "dimensión" in title or "dimension" in title:
            score += 5

    return score


def select_semantic_context(
    user_question: str,
    semantic_context: str,
    max_sections: int = 3,
) -> str:
    sections = extract_sections(semantic_context)

    if not sections:
        return semantic_context

    scored_sections = []

    for section in sections:
        score = score_section(user_question, section)

        scored_sections.append({
            "title": section["title"],
            "content": section["content"],
            "score": score,
        })

    scored_sections = sorted(scored_sections, key=lambda x: x["score"], reverse=True)

    selected = [section for section in scored_sections if section["score"] > 0][:max_sections]

    if not selected:
        return semantic_context

    selected_text = []

    for section in selected:
        selected_text.append(f"""
## {section["title"]}

{section["content"]}
""")

    trace = "\n".join(
        [
            f"- {section['title']} → score {section['score']}"
            for section in scored_sections[:5]
        ]
    )

    return f"""
# Contexto semántico seleccionado

## Trazabilidad de selección

{trace}

{''.join(selected_text)}
"""