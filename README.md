# SophiArch — Course Notebooks

Google Colab notebooks for [SophiArch](https://sophiarch.com) courses.

This repository is public so that notebooks can be opened directly in Google Colab. Course content, platform code, and lesson text live in a separate private repository.

## Structure

Each lab sits at the same path as the lesson it belongs to:

```
content/courses/{course-slug}/{lesson-folder}/lab.ipynb
```

There is one folder per course under `content/courses/`, and at most one lab per lesson. Each notebook opens with a cell that states its lab type (`write`, `debug`, `review`, `extend` or `prompt`), course, lesson and task. The lab type must match the lesson's `lab_type`.

Shared data files live in `datasets/`.

## Contributing

- Notebooks must have all cell outputs cleared before committing.
- Labs must be self-contained: install cell and imports at the top, data generated in the notebook or read from `datasets/`.
- Labs target the package versions Colab ships, because that's what learners run: an unpinned `!pip install` doesn't upgrade a package Colab already has. `pyproject.toml` pins those versions, so the local environment matches Colab. Don't use an API that only exists in a newer release.
- A cell that is meant to raise an error (a `write`-lab stub, a demonstrated failure) needs the `raises-exception` cell tag.

## Testing

```bash
uv sync --group dev
uv run pytest                 # fast checks: outputs cleared
uv run pytest -m execute      # runs every lab end to end (slow)
```

The execution test skips, with a reason, any lab that needs a package that isn't installed, or that downloads models or calls an API (set `LAB_TESTS_NETWORK=1` to include those).

## Keeping up with Colab

Colab updates its runtime periodically. Its package list is published in [googlecolab/backend-info](https://github.com/googlecolab/backend-info/blob/main/pip-freeze.txt) (`pip-freeze.gpu.txt` for the GPU runtime, which is where `torch` has a plain version number). When it changes:

1. Update the pinned versions in `pyproject.toml` to match, then run `uv lock`.
2. Run `uv sync --group dev` and `uv run pytest -m execute`, and fix any lab that fails.
3. Packages Colab doesn't ship (`catboost`, `faiss-cpu`, `rank-bm25`) keep a minimum version; labs install them with `!pip install`.
