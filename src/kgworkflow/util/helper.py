import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Union

from pandas import DataFrame
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import NamespaceManager
import pandas as pd
import rdflib.query as query

logger = logging.getLogger(__name__)


class UserException(Exception):
    pass


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

    try:
        result = graph.query(sparql)
    except Exception as ex:
        logger.error(f"\r\n{sparql}")
        raise UserException("The SPARQL query failed to execute.") from ex

    return result.askAnswer


def sparql_select(
    graph: Graph, sparql: str, to_df: bool = True
) -> Union[DataFrame, query.Result]:
    """
    Executes a SPARQL SELECT query on the given RDF graph and returns the result
    either as a pandas DataFrame or as an RDFLib query result, depending on the
    `to_df` flag.

    :param graph: The RDFLib Graph instance on which the SPARQL query is
        executed.
    :type graph: Graph

    :param sparql: The SPARQL SELECT query to be executed on the RDF graph.
    :type sparql: str

    :param to_df: A boolean flag indicating whether to convert the query results
        to a pandas DataFrame (True) or return them as RDFLib query results
        (False). Defaults to True.
    :type to_df: bool

    :return: If `to_df` is True, returns a pandas DataFrame representation of the
        SPARQL query result with normalized URIs. If `to_df` is False, returns
        an RDFLib query.result instance containing the raw query results.
    :rtype: Union[DataFrame, query.Result]
    """
    try:
        sparql_result = graph.query(sparql)
    except Exception as ex:
        logger.error(f"\r\n{sparql}")
        raise UserException("The SPARQL query failed to execute.") from ex

    if to_df:
        df_result = sr2df(sparql_result)
        normalized_df_result = normalize_uris(df_result, graph.namespace_manager)
        return normalized_df_result
    else:
        return sparql_result


def sr2df(results: query.Result) -> DataFrame:
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
        columns=[str(x) for x in results.vars],
    )


def normalize_uris(df: DataFrame, nsm: NamespaceManager) -> DataFrame:
    """
    Normalizes URIs in a DataFrame by converting them using the given NamespaceManager.

    This function iterates over the elements of the DataFrame, and for each element
    that is a URIRef, it normalizes it using the NamespaceManager. If an element is
    not a URIRef, it remains unmodified. The normalized DataFrame is then returned.

    :param df: The DataFrame to process. Expected to contain values of type URIRef or
        other types that do not require normalization.
    :type df: DataFrame
    :param nsm: The NamespaceManager instance used to normalize URIs.
    :type nsm: NamespaceManager
    :return: A DataFrame where all URIRef elements have been normalized using the
        provided NamespaceManager. Non-URIRef elements are unmodified.
    :rtype: DataFrame
    """

    def convert_uri(val):
        if isinstance(val, URIRef):
            return nsm.normalizeUri(val)
        return val

    return df.map(convert_uri)


def infer_graph(graph: Graph, reasoner: str = "hermit") -> Graph:
    """
    Performs reasoning on a given RDF graph using a specified OWL reasoner
    and returns the inferred graph. The reasoning process entails taking
    the input graph, running the reasoner to deduce additional triples
    based on the ontology, and then returning the extended graph.

    The function uses serialized files to interact with the reasoner,
    and the reasoning is performed on temporary files created during
    runtime. After reasoning, the inferred graph is deserialized and
    returned.

    :param graph: The RDF graph to be inferred.
    :type graph: Graph
    :param reasoner: The name of the OWL reasoner. Defaults to 'hermit'.
    :type reasoner: str
    :return: A graph containing the input triples and the inferred ones.
    :rtype: Graph
    """
    result = Graph()
    with tempfile.NamedTemporaryFile(suffix=".ttl", delete=True) as input_file:
        with tempfile.NamedTemporaryFile(suffix=".ttl", delete=True) as output_file:
            graph.serialize(input_file.name, format="turtle")
            input_file.flush()
            infer_file(input_file.name, output_file.name, reasoner)
            result.parse(output_file.name, format="turtle")
    return result


def infer_file(input_file: str, output_file: str, reasoner: str) -> None:
    """
    Executes reasoning on an input ontology file using a specified reasoner and
    writes the inferred ontology to an output file. The reasoning process
    relies on the ROBOT command-line tool, which must be accessible via the
    `ROBOT` environment variable.

    :param input_file: The file containing the input ontology.
    :type input_file: str
    :param output_file: The file where the inferred ontology will be written.
    :type output_file: str
    :param reasoner: The reasoning engine to be used (e.g., ELK, Hermit).
    :type reasoner: str
    :return: None
    :raises Exception: If the ROBOT environment variable is not set.
    """
    ROBOT = os.getenv("ROBOT")
    if not ROBOT:
        logger.error(
            "ROBOT environment variable not set. You can configure it in .env."
        )
        raise Exception("ROBOT environment variable not set")

    # If you want the results, use res = subprocess.run(
    subprocess.run(
        [
            ROBOT,
            "reason",
            "--input",
            input_file,
            "--output",
            output_file,
            "--create-new-ontology",
            "true",
            "--equivalent-classes-allowed",
            "all",
            "--include-indirect",
            "true",
            "--axiom-generators",
            '"SubClass EquivalentClass DisjointClasses ClassAssertion PropertyAssertion"',
            "--reasoner",
            reasoner,
        ],
        capture_output=True,
        text=True,
    )


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

    if not os.path.exists(filename):
        raise UserException(f"The input Turtle file {filename} does not exist.")

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

    if not os.path.exists(filename):
        raise UserException(f"The SPARQL query file {filename} does not exist.")

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


def write_ttl(
    graph: Graph, filename: str, default_ns: Namespace = None, base: str = None
) -> None:
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
    logger.info(f"Writing graph to {filename}.")
    logger.info(f"Using default namespace {default_ns}.")
    logger.info(f"And base URI {base}.")

    if default_ns:
        graph.bind("", default_ns)

    try:
        with open(filename, "wb") as f:
            graph.serialize(f, format="turtle", base=base)
    except Exception as ex:
        raise UserException(f"Could not write graph to {filename}: {ex}.") from ex
