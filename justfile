RUFF := 'uv run ruff'
TY := 'uv run ty'

format:
    {{ RUFF }} format . --silent
    {{ RUFF }} check . --fix --unsafe-fixes --exit-zero --silent

check:
    {{ RUFF }} check .
    {{ TY }} check .

install:
    uv sync

upgrade:
    uv lock --upgrade

day:
    uv run copier copy _day_template/ . --trust

shell:
    uv run ipython
