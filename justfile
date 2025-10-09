# load .env file
set dotenv-load

default:
  just --list

pip-install:
  @uv pip install --editable .

remove-origin:
  @git remote rm origin

say-hello:
  @echo "Hello!"

solve-zebra:
  @uv run solve-zebra

sparql-select: say-hello
  @uv run sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o output/out.csv

update-requirements:
    @uv pip freeze > requirements.txt

run-notebook file:
    @uv run jupyter execute {{file}}