import logging
import os
import tempfile

from kgworkflow.util.helper import (
    infer_graph,
    get_kg,
    sparql_select,
    get_sparql,
    sparql_ask,
    output_ttl,
    write_ttl,
)
from dotenv import load_dotenv

from kgworkflow.util.setup_logging import setup_logging

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)

logger.info("Running test_kg.py")
logger.debug("Logging is set to INFO level by default.")

TOY = "test/resources/ttl/toy.ttl"
EMPTY = "test/resources/ttl/empty.ttl"


def test_get_kg():
    g = get_kg(TOY)
    assert len(g) > 0

    g = get_kg(EMPTY)
    assert len(g) == 0


def test_reason_hermit():
    query = get_sparql("test/resources/sparql/ask-red-toy.sparql")
    kb = infer_graph(get_kg(TOY), reasoner="hermit")
    output_ttl(kb)
    result = sparql_ask(graph=kb, sparql=query)
    assert result


def test_write_ttl():
    with tempfile.NamedTemporaryFile(suffix=".ttl", delete=True) as output_file:
        write_ttl(get_kg(TOY), output_file.name)
        assert os.path.exists(f"{output_file.name}")


def test_sparql_select():
    query = get_sparql("test/resources/sparql/s-p-o.sparql")
    result = sparql_select(get_kg(TOY), query)
    assert len(result) > 0


def test_sparql_ask():
    query = get_sparql("test/resources/sparql/ask-red-toy.sparql")

    kg = get_kg("test/resources/ttl/inferred-toy.ttl")
    result = sparql_ask(graph=kg, sparql=query)
    assert result

    kg = get_kg(TOY)
    result = sparql_ask(graph=kg, sparql=query)
    assert not result
