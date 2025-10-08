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

def test_get_kb():
    g = get_kg("util-test")
    assert len(g) > 0

    g = get_kg("empty")
    assert len(g) == 0


def test_reason_hermit():
    result = reason(get_kg("toy"))
    output_ttl(result)
    assert len(result) > 0


def test_write_ttl():
    with tempfile.NamedTemporaryFile(suffix='.ttl', delete=True) as output_file:
        write_ttl(get_kg("util-test"), output_file.name)
        assert os.path.exists(
            f"{output_file.name}"
        )


def test_sparql_df():
    query = get_sparql("s-p-o")
    result = sparql_df(query, get_kg("util-test"))
    assert len(result) > 0


def test_sparql_ask():
    query = get_sparql("ask")

    kb = get_kg("util-test")
    result = sparql_ask(sparql=query, graph=kb)
    assert result == True

    kb = get_kg("empty")
    result = sparql_ask(sparql=query, graph=kb)
    assert result == False


if __name__ == '__main__':
    pass
