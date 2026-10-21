"""Execute every lab notebook and fail on any unexpected error.

Opt-in, because a full run takes a while: `uv run pytest -m execute`.

A lab is skipped, with the reason, when it imports a package that isn't installed or needs the
network (model downloads, API keys) and LAB_TESTS_NETWORK=1 isn't set. `!pip` lines are not run:
the test checks the code against the installed versions. To check against the versions Colab
ships, see "Testing" in README.md.

A cell that is meant to raise (a `write`-lab stub, a demonstrated error) must carry the
`raises-exception` cell tag.
"""

import ast
import importlib.util
import os
import sys
from pathlib import Path

import pytest

nbformat = pytest.importorskip("nbformat")
nbclient = pytest.importorskip("nbclient")

REPO = Path(__file__).resolve().parent.parent
_NOTEBOOKS = sorted((REPO / "content").rglob("lab.ipynb"))

# Packages whose labs download models or data, or call a paid API.
NEEDS_NETWORK = {"anthropic", "datasets", "google", "httpx", "sentence_transformers", "transformers"}

# Labs read the shared dataset from this repo on GitHub; point them at the local copy instead.
DATASETS_URL = "https://raw.githubusercontent.com/SophiArch/notebooks/main/datasets/"


def _code(cell_source: str) -> str:
    return "\n".join(
        ("pass  # " + line) if line.lstrip().startswith(("!", "%")) else line
        for line in cell_source.splitlines()
    )


def _imports(nb) -> set[str]:
    names = set()
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        for node in ast.walk(ast.parse(_code(cell.source))):
            if isinstance(node, ast.Import):
                names.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                names.add(node.module.split(".")[0])
    return names - set(sys.stdlib_module_names)


@pytest.mark.execute
@pytest.mark.parametrize("notebook_path", _NOTEBOOKS, ids=lambda p: str(p.parent.relative_to(REPO / "content")))
def test_notebook_executes(notebook_path: Path, tmp_path: Path) -> None:
    nb = nbformat.read(notebook_path, as_version=4)
    imports = _imports(nb)

    missing = sorted(m for m in imports if importlib.util.find_spec(m) is None)
    if missing:
        pytest.skip(f"needs {', '.join(missing)}")
    network = sorted(imports & NEEDS_NETWORK)
    if network and os.environ.get("LAB_TESTS_NETWORK") != "1":
        pytest.skip(f"needs network ({', '.join(network)}); set LAB_TESTS_NETWORK=1 to run")

    local_datasets = (REPO / "datasets").as_posix() + "/"
    for cell in nb.cells:
        if cell.cell_type == "code":
            cell.source = _code(cell.source).replace(DATASETS_URL, local_datasets)

    client = nbclient.NotebookClient(
        nb,
        timeout=600,
        kernel_name="python3",
        resources={"metadata": {"path": str(tmp_path)}},
    )
    try:
        client.execute()
    except nbclient.exceptions.CellExecutionError as err:
        pytest.fail(f"{notebook_path.relative_to(REPO)}: {str(err)[-1500:]}", pytrace=False)
