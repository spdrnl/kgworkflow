import os

from kgworkflow.helpers.general_helper import get_project_root, logger, UserException
from rdflib import Graph, Namespace


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
        logger.info(ex)
        raise UserException(f"Could not write graph to {filename}: {ex}.") from ex


def read_ttl_kg(filename: str) -> Graph:
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
