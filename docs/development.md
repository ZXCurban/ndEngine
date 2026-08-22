# Development

## Stack

- Python
- uv
- Ruff
- Pytest
- Mypy

## Setup

```bash
uv sync
```

## Check

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest
```

## Format

```bash
uv run ruff format .
```

## Development order

1. Math
2. Geometry
3. Transform
4. Projection
5. Renderer
6. TUI

## Rule
Сначала простая универсальная абстракция.
Специальные случаи добавлять только при реальной необходимости.