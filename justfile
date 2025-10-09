# load .env file
set dotenv-load

default:
  just --list

robot-test:
  @sh robot-test.sh

install:
  @uv pip install --editable .

remove-origin:
  @git remote rm origin

say-hello:
  @echo "Hello!"

solve-zebra:
  @uv run solve-zebra

sparql-select: say-hello
  @uv run sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o output/out.csv