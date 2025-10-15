set dotenv-load := true

default:
    just --list

# Runs pip-install after.
install-project: && pip-install
    @uv venv
    @uv sync

pip-install:
    @uv pip install --editable .

install-arq:
    echo "Installing Apache Jena in ext-bin/jena"
    wget $APACHE_JENA_URL
    @mkdir -p ext-bin
    @unzip -o -q -d ext-bin apache-jena-*.zip
    @rm -rf ext-bin/jena
    @mv ext-bin/apache-jena* ext-bin/jena
    @rm apache-jena-*.zip

update-requirements:
    @uv pip freeze > requirements.txt

remove-origin:
    @git remote rm origin

say-hello:
    @echo "Hello!"
    @just default

solve-zebra:
    @uv run solve-zebra

sparql-select:
    @uv run sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o output/out.csv

run-test:
    @uv run pytest

run-notebook file:
    @uv run jupyter execute {{ file }}

run-python:
    #!/usr/bin/env -S uv run --script --quiet
    from kgworkflow.helpers.sparql_helper import read_sparql
    print(read_sparql("input/sparql/zebra.sparql"))

run-ruff:
    @pre-commit run --all-files

format-turtle:
    @turtlefmt test/resources/ttl/ input/ttl output

hermit-instance-profile input_file output_file:
    robot reason \
    --input {{ input_file}} \
    --create-new-ontology true \
    --equivalent-classes-allowed all \
    --axiom-generators "SubClass EquivalentClass DisjointClasses ClassAssertion PropertyAssertion" \
    --output {{ output_file }} \
    --include-indirect true \
    --reasoner hermit