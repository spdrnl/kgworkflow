set dotenv-load := true

default:
    just --list

install-project:
    @uv venv
    @uv sync
    @uv pip install --editable .

pip-install:
    @uv pip install --editable .

update-requirements:
    @uv pip freeze > requirements.txt

remove-origin:
    @git remote rm origin

say-hello:
    @echo "Hello!"

solve-zebra:
    @uv run solve-zebra

sparql-select: say-hello
    @uv run sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o output/out.csv

run-test:
    @uv run pytest

run-notebook file:
    @uv run jupyter execute {{ file }}

run-python:
    #!/usr/bin/env -S uv run --script --quiet
    from kgworkflow.util.helper import get_sparql
    print(get_sparql("src/resources/sparql/zebra.sparql"))
