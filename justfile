RUN := 'uv run --frozen'

format:
    {{ RUN }} ruff format . --silent
    {{ RUN }} ruff check . --fix --unsafe-fixes --exit-zero --silent

check:
    {{ RUN }} ruff check .
    {{ RUN }} ty check .

install:
    uv sync

upgrade:
    uv lock --upgrade --exclude-newer '7 days ago'

day:
    {{ RUN }} copier copy _day_template/ . --trust

shell:
    {{ RUN }} ipython

test *args:
    {{ RUN }} pytest -s -v {{ args }}

run *args:
    {{ RUN }} python {{ args }}
