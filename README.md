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
- Code must run on the package versions Colab ships, not only on the latest releases. Learners run labs in Colab, and an unpinned `!pip install` doesn't upgrade a package Colab already has. Colab publishes its package list in [googlecolab/backend-info](https://github.com/googlecolab/backend-info/blob/main/pip-freeze.txt).
- A cell that is meant to raise an error (a `write`-lab stub, a demonstrated failure) needs the `raises-exception` cell tag.

## Testing

```bash
uv sync --group dev
uv run pytest                 # fast checks: outputs cleared
uv run pytest -m execute      # runs every lab end to end (slow)
```

The execution test skips, with a reason, any lab that needs a package that isn't installed, or that downloads models or calls an API (set `LAB_TESTS_NETWORK=1` to include those). To check the labs against Colab's versions as well, run the same test in a separate environment with Colab's versions of the core packages (take the current versions from Colab's `pip-freeze.txt`):

```bash
uv venv .venv-colab
uv pip install -p .venv-colab pandas==2.2.3 scikit-learn==1.6.1 numpy==2.1.3 \
    matplotlib seaborn scipy statsmodels pydantic pytest nbclient nbformat ipykernel
.venv-colab/bin/python -m pytest -m execute
```
