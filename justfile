RUN := 'uv run --frozen'
CUTOFF := '"7 days ago"'

format:
    {{ RUN }} ruff format . --silent
    {{ RUN }} ruff check . --fix --unsafe-fixes --exit-zero --silent

check:
    {{ RUN }} ruff check .
    {{ RUN }} ty check .

install *packages:
    uv add --exclude-newer {{ CUTOFF }} {{ packages }}

sync:
    uv sync --frozen

lock:
    uv lock --exclude-newer {{ CUTOFF }}

upgrade:
    uv lock --upgrade --exclude-newer {{ CUTOFF }}

day:
    {{ RUN }} copier copy _day_template/ . --trust

shell:
    {{ RUN }} ipython

test *args:
    {{ RUN }} pytest -s -v {{ args }}

run *args:
    {{ RUN }} python {{ args }}
