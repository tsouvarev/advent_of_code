RUN := 'uv run --frozen'
WITH_CUTOFF := '--exclude-newer "7 days ago"'

format:
    {{ RUN }} ruff format . --silent
    {{ RUN }} ruff check . --fix --unsafe-fixes --exit-zero --silent

check:
    {{ RUN }} ruff check .
    {{ RUN }} ty check .

install *packages:
    uv add {{ WITH_CUTOFF }} {{ packages }}

sync:
    uv sync --frozen

lock:
    uv lock {{ WITH_CUTOFF }}

upgrade:
    uv lock --upgrade {{ WITH_CUTOFF }}

outdated:
    uv pip list --outdated {{ WITH_CUTOFF }}

day:
    {{ RUN }} copier copy _day_template/ . --trust

shell:
    {{ RUN }} ipython

test *args:
    {{ RUN }} pytest -s -v {{ args }}

run *args:
    {{ RUN }} python {{ args }}
