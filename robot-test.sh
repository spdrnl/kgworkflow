robot reason \
  --input test/resources/ttl/toy.ttl \
  --create-new-ontology true \
  --equivalent-classes-allowed all\
  --axiom-generators "SubClass EquivalentClass DisjointClasses ClassAssertion PropertyAssertion" \
  --output output/toy-inferred.ttl \
  --include-indirect true \
  --reasoner hermit