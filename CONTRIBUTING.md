# Contributing to arcane

Thank you for your interest in the project! `main` is protected: every change
goes through a pull request.

## Workflow

1. **Open an issue** describing the bug or the feature (use the templates).
2. **Create a branch** from an up-to-date `main`, named after its purpose:
   `feature/...`, `fix/...`, `docs/...`, `chore/...` or `ci/...`.
3. **Develop with small commits**, one per function or per topic, using the
   [Conventional Commits](https://www.conventionalcommits.org/) format, for
   example `feat(analysis): add by_extension()`.
4. **Check your work locally** (see below).
5. **Push the branch and open a pull request** toward `main`. Link the issue
   with `Closes #<number>` in the description.
6. **Address the review**, pushing new commits to the same branch.
7. The pull request is merged with **Squash and merge**, and only when every
   CI job is green.

## Local setup

```bash
pip install -e ".[dev]"
pre-commit install
```

## Checks

```bash
pytest --cov=arcane         # tests and coverage
pre-commit run --all-files  # Black, Ruff and file checks
```

The CI runs two jobs on every pull request: `pre-commit` (formatting and
linting) and `tests` (the test suite on several Python versions).

## Code guidelines

- Write NumPy-style docstrings (`Parameters`, `Returns`, `Raises`, `Examples`).
- Keep the implementation in internal modules (prefixed with `_`) and expose the
  public API in the `__init__.py` files.
- Put the tests in the `tests/` folder of the submodule they verify.
- Cover normal cases, edge cases and expected exceptions.

## Branch protection

The `main` branch requires a pull request and the `pre-commit` and `tests`
status checks before merging. Direct pushes to `main` are blocked.
