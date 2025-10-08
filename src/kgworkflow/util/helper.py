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


def sparql_ask(graph: Graph, sparql: str) -> bool:
    """
    Executes a SPARQL ASK query on the given RDF graph and returns the result as
    a boolean value. The function evaluates whether the query condition is
    satisfied within the provided graph.

    :param graph: The RDF graph on which to execute the SPARQL ASK query.
    :type graph: rdflib.Graph
    :param sparql: The SPARQL ASK query string to evaluate against the graph.
    :type sparql: str
    :return: The boolean result of the SPARQL ASK query.
    :rtype: bool
    """
    result = graph.query(sparql)
    return result.askAnswer


def sparql_select(graph: Graph, sparql: str) -> DataFrame:
    """
    Executes a SPARQL SELECT query on the given graph and returns the results as a
    normalized DataFrame. The method utilizes helper functions to convert the
    SPARQL query results into a pandas DataFrame format and normalizes URIs within
    the DataFrame according to the graph context.

    :param graph: The RDF graph on which the SPARQL query will be executed.
    :type graph: Graph
    :param sparql: The SPARQL query string to be executed on the RDF graph.
    :type sparql: str
    :return: A DataFrame containing the results of the executed SPARQL query with
        normalized URIs.
    :rtype: DataFrame
    """
    sparqlResult = graph.query(sparql)
    df_result = sparql_results_to_df(sparqlResult)
    normalized_df_result = normalize_uris(df_result, graph)
    return normalized_df_result


def sparql_results_to_df(results: SPARQLResult) -> DataFrame:
    """
    Converts a SPARQL query result set into a pandas DataFrame. The utility extracts
    values from SPARQLResult rows and converts them into a tabular format. Each
    value in the resulting DataFrame retains its appropriate Python type.

    :param results: SPARQL query result set containing rows of variable bindings.
    :type results: SPARQLResult
    :return: A pandas DataFrame representing the SPARQL query result set, where
        each column corresponds to a SPARQL variable and rows represent variable
        bindings transformed to their Python-native types.
    :rtype: DataFrame
    """
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
    """
    Normalizes URIs in a DataFrame using the namespace manager of a provided RDF graph.

    This function takes a DataFrame and an RDF graph as inputs. It applies the
    namespace manager from the graph to normalize any `URIRef` values found in
    the DataFrame. Non-`URIRef` values remain unchanged.

    :param df: The input DataFrame containing data to be processed.
    :type df: DataFrame
    :param graph: The RDF graph providing the namespace manager for URI normalization.
    :type graph: Graph
    :return: A DataFrame with normalized URIs, where applicable.
    :rtype: DataFrame
    """
    nm = graph.namespace_manager

    def convert_uri(val):
        if isinstance(val, URIRef):
            return nm.normalizeUri(val)
        return val

    return df.map(convert_uri)


def reason(graph: Graph, reasoner: str = 'hermit') -> Graph:
    """
    Applies reasoning to an RDF graph using the ROBOT command-line tool and a specified reasoner.

    The function reads an input RDF graph, reasons over it using the specified
    reasoning engine, and produces an augmented RDF graph with inferred triples.
    It leverages the ROBOT environment variable for accessing the command-line
    tool, and the tool's reasoning options are configured appropriately.

    :param graph: An RDF graph that will serve as the input for reasoning.
    :type graph: Graph
    :param reasoner: The reasoning engine to use, such as 'hermit' or other supported tools. Defaults to 'hermit'.
    :type reasoner: str
    :return: A new RDF graph containing the input data alongside inferred triples.
    :rtype: Graph
    """

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
    """
    Parses a Turtle-formatted RDF file and returns its corresponding RDF graph.

    This function utilizes the RDFLib library to parse an RDF file in Turtle format
    and constructs a corresponding RDF graph object. The graph is useful for performing
    operations such as querying, reasoning, or manipulating RDF data.

    :param filename: Path to the file containing the RDF data in Turtle format.
    :type filename: str
    :return: Graph object representing the parsed RDF data.
    :rtype: Graph
    """
    g = Graph()
    g.parse(filename, format="turtle")
    return g


def get_sparql(filename: str) -> str:
    """
    Reads and returns the content of a SPARQL query file.

    :param filename: The path to the SPARQL query file.
    :type filename: str
    :return: The content of the SPARQL query file as a string.
    :rtype: str
    """
    with open(filename) as f:
        return f.read()


def get_project_root() -> Path:
    """
    Returns the root directory of the project.

    This function computes the root directory of the project
    by moving up four levels in the directory structure
    from the current module's absolute path.

    :return: The root directory of the project.
    :rtype: Path
    """
    return Path(os.path.abspath(__file__)).parent.parent.parent.parent


def output_ttl(graph: Graph) -> None:
    """
    Generates a Turtle (TTL) representation of the provided RDF graph and outputs it to
    a predefined file location. It checks for an environment variable "DEFAULT_NAMESPACE"
    to define a namespace for the graph, if set. The output file is written in the "output"
    directory relative to the project root.

    :param graph: A Graph object representing the RDF data.
    :type graph: Graph
    :return: None
    """
    base = None
    default_ns = None
    if os.getenv("DEFAULT_NAMESPACE"):
        default_ns = Namespace(os.getenv("DEFAULT_NAMESPACE"))

    output_file = f"{get_project_root()}/output/out.ttl"
    write_ttl(graph, output_file, default_ns, base)


def write_ttl(graph: Graph, filename: str, default_ns: Namespace = None, base: str = None) -> None:
    """
    Writes an RDF graph to a Turtle (.ttl) file with optional default namespace
    and base URI configuration.

    This function allows serializing an RDF graph object to the Turtle format
    and writing it to a file. A default namespace can optionally be bound to
    the graph, and a base URI can also be specified for serialization.

    :param graph: The RDF graph to be serialized and written to the file.
    :type graph: Graph
    :param filename: The path to the file where the Turtle data will be written.
    :type filename: str
    :param default_ns: Optional default namespace to bind to the graph.
    :type default_ns: Namespace, optional
    :param base: Optional base URI to use during serialization.
    :type base: str, optional
    :return: This method does not return any value.
    :rtype: None
    """
    logger.debug(f"Writing graph to {filename}")

    if default_ns:
        graph.bind("", default_ns)

    with open(filename, "wb") as f:
        graph.serialize(f, format="turtle", base=base)
