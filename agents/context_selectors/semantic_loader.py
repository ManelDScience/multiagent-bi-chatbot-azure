from pathlib import Path


def find_project_root() -> Path:
    current = Path(__file__).resolve()

    for parent in current.parents:
        if (parent / "semantic-layer").exists():
            return parent

    raise FileNotFoundError("No se encontró la carpeta semantic-layer.")


def read_file_if_exists(path: Path) -> str:
    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8")


def load_semantic_context() -> str:
    project_root = find_project_root()
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
            sections.append(f"""## {title}

{content}
""")

    if not sections:
        return "No hay contexto semántico disponible."

    return "\n".join(sections)