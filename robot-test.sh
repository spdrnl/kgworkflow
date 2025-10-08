robot reason \
  --input test/resources/ttl/toy.ttl \
  --create-new-ontology true \
  --equivalent-classes-allowed all\
  --axiom-generators "SubClass EquivalentClass DisjointClasses ClassAssertion PropertyAssertion" \
  --output out.ttl \
  --include-indirect true \
  --reasoner hermit