RUFF := 'uv run --frozen ruff'
TY := 'uv run --frozen ty'

format:
    {{ RUFF }} format . --silent
    {{ RUFF }} check . --fix --unsafe-fixes --exit-zero --silent

check:
    {{ RUFF }} check .
    {{ TY }} check .

install:
    uv sync

upgrade:
    uv lock --upgrade --exclude-newer `date --date '7 days ago' --iso-8601`

day:
    uv run copier copy _day_template/ . --trust

shell:
    uv run ipython
