import os
from typing import Union

import pandas as pd
from kgworkflow.helpers.general_helper import logger, UserException
from pandas import DataFrame
from rdflib import Graph, query as query, URIRef
from rdflib.namespace import NamespaceManager


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
        logger.info(ex)
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
        logger.info(ex)
        logger.error(f"\r\n{sparql}")
        raise UserException("The SPARQL query failed to execute.") from ex

    if to_df:
        df_result = sparql_result_to_df(sparql_result)
        normalized_df_result = normalize_uris(df_result, graph.namespace_manager)
        return normalized_df_result
    else:
        return sparql_result


def sparql_result_to_df(results: query.Result) -> DataFrame:
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


def read_sparql(filename: str) -> str:
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
