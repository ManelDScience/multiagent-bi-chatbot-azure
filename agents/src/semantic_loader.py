from pathlib import Path


def read_file_if_exists(path: Path) -> str:
    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8")


def load_semantic_context() -> str:
    project_root = Path(__file__).resolve().parents[2]

    semantic_path = project_root / "semantic-layer"

    files = {
        "MÉTRICAS": semantic_path / "metrics.md",
        "DIMENSIONES": semantic_path / "dimensions.md",
        "REGLAS DE NEGOCIO": semantic_path / "business_rules.md",
    }

    sections = []

    for title, path in files.items():
        content = read_file_if_exists(path)

        if content:
            sections.append(f"""
## {title}

{content}
""")

    if not sections:
        return "No hay contexto semántico disponible."

    return "\n".join(sections)