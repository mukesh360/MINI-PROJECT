import sys
from pathlib import Path

# Always point to project root explicitly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
