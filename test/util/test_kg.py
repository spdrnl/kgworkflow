import logging
import os
import tempfile

from util.kg import reason, get_kg, sparql_df, get_sparql, sparql_ask, output_ttl, write_ttl
from dotenv import load_dotenv

from util.setup_logging import setup_logging

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)

logger.info("Running test_kg.py")
logger.debug("Logging is set to INFO level by default.")

TOY_KB = "test/resources/ttl/toy.ttl"
EMPTY_TTL = "test/resources/ttl/empty.ttl"

def test_get_kb():
    g = get_kg(TOY_KB)
    assert len(g) > 0

    g = get_kg(EMPTY_TTL)
    assert len(g) == 0


def test_reason_hermit():
    result = reason(get_kg(TOY_KB), reasoner='hermit')
    output_ttl(result)
    assert len(result) > 0


def test_write_ttl():
    with tempfile.NamedTemporaryFile(suffix='.ttl', delete=True) as output_file:
        write_ttl(get_kg(TOY_KB), output_file.name)
        assert os.path.exists(
            f"{output_file.name}"
        )


def test_sparql_df():
    query = get_sparql("test/resources/sparql/s-p-o.sparql")
    result = sparql_df(query, get_kg(TOY_KB))
    assert len(result) > 0


def test_sparql_ask():
    query = get_sparql("test/resources/sparql/ask.sparql")

    kb = get_kg(TOY_KB)
    result = sparql_ask(sparql=query, graph=kb)
    assert result == True

    kb = get_kg(EMPTY_TTL)
    result = sparql_ask(sparql=query, graph=kb)
    assert result == False


if __name__ == '__main__':
    pass
