robot-test:
    @sh robot-test.sh

say-hello:
    @echo "Hello!"

sparql-select-test: say-hello
    @uv run sparql-select -q test/resources/sparql/s-p-o.sparql -i test/resources/ttl/toy.ttl -o out.csv