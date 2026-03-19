"""Verify all notebooks have no pre-run outputs before committing."""

import json
from pathlib import Path

import pytest

_NOTEBOOKS = sorted(Path("content").rglob("lab.ipynb"))


@pytest.mark.parametrize("notebook_path", _NOTEBOOKS, ids=lambda p: str(p.parent))
def test_notebook_has_no_pre_run_outputs(notebook_path: Path) -> None:
    nb = json.loads(notebook_path.read_text())
    for i, cell in enumerate(nb["cells"]):
        assert cell.get("outputs", []) == [], f"Cell {i} has outputs in {notebook_path}"
        assert cell.get("execution_count") is None, (
            f"Cell {i} has execution_count in {notebook_path}"
        )
