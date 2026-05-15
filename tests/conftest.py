import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = PROJECT_ROOT / "agents"

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(AGENTS_DIR))