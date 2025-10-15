import os
import subprocess
import tempfile

from kgworkflow.helpers.general_helper import logger
from rdflib import Graph


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
