import logging
import os
import subprocess
import tempfile
from pathlib import Path

from pandas import DataFrame
from rdflib import Graph, URIRef, Namespace
from rdflib.plugins.sparql.processor import SPARQLResult
import pandas as pd

logger = logging.getLogger(__name__)


def sparql_ask(graph, sparql) -> bool:
    result = graph.query(sparql)
    return result.askAnswer


def sparql_select(graph: Graph, sparql: str) -> DataFrame:
    sparqlResult = graph.query(sparql)
    df_result = sparql_results_to_df(sparqlResult)
    normalized_df_result = normalize_uris(df_result, graph)
    return normalized_df_result


def sparql_results_to_df(results: SPARQLResult) -> DataFrame:
    def get_value(x):
        if x is None:
            return None
        elif isinstance(x, URIRef):
            return x
        else:
            return x.toPython()

    return pd.DataFrame(
        data=([get_value(x) for x in row] for row in results),
        columns=[str(x) for x in results.vars]
    )


def normalize_uris(df: DataFrame, graph: Graph) -> DataFrame:
    nm = graph.namespace_manager

    def convert_uri(val):
        if isinstance(val, URIRef):
            return nm.normalizeUri(val)
        return val

    return df.map(convert_uri)


def reason(graph: Graph, reasoner: str = 'hermit') -> Graph:
    """Run robot reason with a temporary output; return result on success."""

    ROBOT = os.getenv("ROBOT")
    if not ROBOT:
        logger.error("ROBOT environment variable not set")
        raise Exception("ROBOT environment variable not set")

    result = Graph()
    with tempfile.NamedTemporaryFile(suffix=".ttl", delete=True) as input_file:
        with tempfile.NamedTemporaryFile(suffix=".ttl", delete=True) as output_file:
            graph.serialize(input_file.name, format="turtle")
            input_file.flush()
            res = subprocess.run(
                [
                    ROBOT, "reason",
                    "--input", input_file.name,
                    "--output", output_file.name,
                    "--create-new-ontology", "true",
                    "--equivalent-classes-allowed", "all",
                    "--include-indirect", "true",
                    "--axiom-generators",
                    "\"SubClass EquivalentClass DisjointClasses ClassAssertion PropertyAssertion\"",
                    "--reasoner", reasoner,
                ],
                capture_output=True,
                text=True,
            )
            result.parse(output_file.name, format="turtle")
    return result


def get_kg(filename: str) -> Graph:
    g = Graph()
    g.parse(filename, format="turtle")
    return g


def get_sparql(filename: str) -> str:
    with open(filename) as f:
        return f.read()


def get_project_root() -> Path:
    return Path(os.path.abspath(__file__)).parent.parent.parent


def output_ttl(graph: Graph) -> None:
    base = None
    default_ns = None
    if os.getenv("DEFAULT_NAMESPACE"):
        default_ns = Namespace(os.getenv("DEFAULT_NAMESPACE"))

    output_file = f"{get_project_root()}/out.ttl"
    write_ttl(graph, output_file, default_ns, base)


def write_ttl(graph: Graph, filename: str, default_ns: Namespace = None, base: str = None) -> None:
    logger.debug(f"Writing graph to {filename}")

    if default_ns:
        graph.bind("", default_ns)

    with open(filename, "wb") as f:
        graph.serialize(f, format="turtle", base=base)
