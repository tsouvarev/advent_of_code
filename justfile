format:
    uv run ruff format . --silent
    uv run ruff check . --fix --unsafe-fixes --exit-zero --silent

check:
    uv run ruff check .
