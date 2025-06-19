RUFF := 'uv run ruff'

format:
    {{ RUFF }} format . --silent
    {{ RUFF }} check . --fix --unsafe-fixes --exit-zero --silent

check:
    {{ RUFF }} check .

install:
	uv sync

upgrade:
	uv lock --upgrade
