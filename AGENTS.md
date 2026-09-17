# AGENTS.md — instructions for agents in this project

> This file MUST NOT end up in `.gitignore`. It is required to stay in the repository.

## Roles

- Lead developer — the user. Only they write and change business logic.
- Agent — reviewer and quality assistant: inspects the diff, covers code with tests,
  runs checks, prepares the project for commit, writes a report.

## Main rule

**DO NOT change code logic.** Changing the behavior of `src/` is forbidden.
The agent is allowed to:

- add/edit files in `tests/`;
- run `ruff check --fix` (imports/obvious autofixes only) and `ruff format`;
- edit `.gitignore` (only by adding standard junk patterns);
- create/edit this `AGENTS.md`.

Anything requiring logic or type fixes in `src/` (including fixes for `mypy --strict`),
the agent does NOT fix, but records in the report under "Bugs / remarks".

**Tests must not be fitted to the current implementation if it contradicts the obvious contract/API.**

Tests must verify the expected contract/API, not merely reproduce
the current implementation. If behavior is ambiguous or the contract is undefined,
the agent records it in the report and does not invent semantics on its own.

## Agent workflow (every run)

1. **Diff:** `git status --short`, `git log --oneline -10`, `git diff --stat`,
   `git diff -- <files>` — understand which features/code were added.
2. **Tests for new code:** if new code in `src/` is uncovered — add tests
   in `tests/` in the existing style (`test_*.py`, `test_*() -> None` functions,
   `pytest.raises` for errors). Name new files by meaning,
   e.g. `tests/test_matrix_setitem.py`.
3. **Checks (all via `uv run`):**
   - `uv run pytest -q`
   - `uv run ruff check .`
   - `uv run ruff format --check .` (on mismatch — `uv run ruff format .`)
   - `uv run mypy src`
4. **Prepare for commit:** check `.gitignore` (must ignore `__pycache__/`,
   `*.py[cod]`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.venv/`,
   `build/`, `dist/`, `.env*`, IDE/OS junk). Make sure `AGENTS.md`,
   `src/`, `tests/` are not ignored (`git check-ignore -v <file>`).
5. **Report + commit name** (see format below). Do NOT commit/push without an explicit request.

## Commands

```bash
uv sync
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
uv run mypy src
git status --short && git diff --stat
```

## Report format

- **Changed code:** what was added (files, methods).
- **Bugs/errors:** list with `file:line` paths, no logic fixes.
- **New tests:** which file, how many tests, what they cover.
- **Linters/formatters:** what was fixed (`ruff check --fix`, `ruff format`).
- **Checks:** `pytest` / `ruff check` / `ruff format --check` / `mypy` — green or not
  (with error output if red).
- **Commit name:** one line in conventional commits style, e.g.
  `feat: ...`, `test: ...`, `chore: ...`.
