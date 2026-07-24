import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))


@pytest.fixture
def tmp_csv(tmp_path: Path) -> Path:
    """Create a temporary CSV file path."""
    return tmp_path / "users.csv"
