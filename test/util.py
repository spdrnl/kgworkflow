import subprocess
import tempfile

from pandas import DataFrame
from rdflib import Graph, URIRef
from rdflib.plugins.sparql.processor import SPARQLResult
import pandas as pd

from dotenv import load_dotenv

load_dotenv()


def sparql_ask(sparql, graph) -> bool:
    result = graph.query(sparql)
    return result.askAnswer


def sparql_df(sparql, graph) -> DataFrame:
    result = graph.query(sparql)
    df_result = sparql_results_to_df(result)
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

    return df.applymap(convert_uri)


def reason(graph: Graph, reasoner: str = 'hermit') -> Graph:
    """Run robot reason with a temporary output; return True on success."""
    g = Graph()
    # robot requires an --output, so use a temp file and let it vanish
    with tempfile.NamedTemporaryFile(suffix=".ttl", delete=True) as input_file:
        with tempfile.NamedTemporaryFile(suffix=".ttl", delete=True) as output_file:
            graph.serialize(input_file.name, format="turtle")
            input_file.flush()
            res = subprocess.run(
                [
                    "/home/sanne/Apps/robot/robot", "reason",
                    "--reasoner", reasoner,
                    "--input", input_file.name,
                    "--output", output_file.name,
                ],
                capture_output=True,
                text=True,
            )
            g.parse(output_file.name, format="turtle")
    return g


def expand_path(filename: str, type: str = "ttl") -> str:
    return f"test/{type}/{filename}.{type}"


def get_kb(filename: str) -> Graph:
    g = Graph()
    g.parse(expand_path(filename), format="turtle")
    return g


def get_sparql(filename: str) -> str:
    with open(expand_path(filename, "sparql")) as f:
        return f.read()
