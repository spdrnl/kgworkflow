import logging
import os
import tempfile

from kgworkflow.helpers.ttl_helper import output_ttl, write_ttl, read_ttl_kg
from kgworkflow.helpers.reasoner_helper import infer_graph
from kgworkflow.helpers.sparql_helper import sparql_ask, sparql_select, read_sparql
from dotenv import load_dotenv

from kgworkflow.logging.setup_logging import setup_logging

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)

logger.info("Running test_kg.py")
logger.debug("Logging is set to INFO level by default.")

TOY = "test/resources/ttl/toy.ttl"
EMPTY = "test/resources/ttl/empty.ttl"


def test_get_kg():
    g = read_ttl_kg(TOY)
    assert len(g) > 0

    g = read_ttl_kg(EMPTY)
    assert len(g) == 0


def test_reason_hermit():
    query = read_sparql("test/resources/sparql/ask-red-toy.sparql")
    kb = infer_graph(read_ttl_kg(TOY), reasoner="hermit")
    output_ttl(kb)
    result = sparql_ask(graph=kb, sparql=query)
    assert result


def test_write_ttl():
    with tempfile.NamedTemporaryFile(suffix=".ttl", delete=True) as output_file:
        write_ttl(read_ttl_kg(TOY), output_file.name)
        assert os.path.exists(f"{output_file.name}")


def test_sparql_select():
    query = read_sparql("test/resources/sparql/s-p-o.sparql")
    result = sparql_select(read_ttl_kg(TOY), query)
    assert len(result) > 0


def test_sparql_ask():
    query = read_sparql("test/resources/sparql/ask-red-toy.sparql")

    kg = read_ttl_kg("test/resources/ttl/inferred-toy.ttl")
    result = sparql_ask(graph=kg, sparql=query)
    assert result

    kg = read_ttl_kg(TOY)
    result = sparql_ask(graph=kg, sparql=query)
    assert not result
