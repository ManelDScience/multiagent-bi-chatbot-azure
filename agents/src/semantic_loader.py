from pathlib import Path

def load_semantic_context() -> str:
    project_root = Path(__file__).resolve().parents[2]

    metrics_path = project_root / "semantic_layer" / "metrics.md"

    if not metrics_path.exists():
        return "No hay contenido semántico disponible."
    
    return metrics_path.read_text(encoding="utf-8")