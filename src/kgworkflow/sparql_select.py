import argparse
import logging
import time

from dotenv import load_dotenv
from pandas import DataFrame

from kgworkflow.util.helper import get_sparql, sparql_select, get_kg, UserException
from kgworkflow.util.setup_logging import setup_logging

# Get settings from .env
load_dotenv()

# Logging
setup_logging()
logger = logging.getLogger(__name__)


def get_args() -> argparse.Namespace:
    """
    Fetches command-line arguments required for processing SPARQL query files against Turtle files
    and outputs the results into a CSV file. Parses the provided arguments and validates their
    presence and expected types.

    :raises SystemExit: If required arguments are missing or invalid arguments are passed.

    :return: Namespace object containing parsed command-line arguments.
    :rtype: argparse.Namespace
    """
    # Initialize
    parser = argparse.ArgumentParser(
        description="The program executes a SPARQL query file against a Turtle file and outputs the results as CSV.",
        epilog="Happy querying!",
        prog="sparql-select",
    )

    # Adding optional parameters
    parser.add_argument(
        "-q", "--query-file", help="SPARQL query file.", required=True, type=str
    )

    parser.add_argument(
        "-i", "--input-file", help="Turtle input file.", required=True, type=str
    )

    parser.add_argument(
        "-o", "--output-file", help="Csv output file.", required=True, type=str
    )

    return parser.parse_args()


def main():
    """
    Executes the main program workflow.

    This executes a SPARQL query using provided files, writes the result to
    an output file.

    :return: None
    """
    # Resolve the arguments
    args = get_args()
    query_file = args.query_file
    input_file = args.input_file
    output_file = args.output_file

    # Echo settings
    logger.info(f"Query file: {query_file}")
    logger.info(f"Input file: {input_file}")
    logger.info(f"Output file: {output_file}")

    # Execute the query
    start_time = time.time()

    df = run_query(input_file, query_file)
    write_csv(df, output_file)

    end_time = time.time()
    logger.info(f"Done in {end_time - start_time:0.3f} seconds.")


def write_csv(df, output_file):
    """
    Writes the provided dataframe to a CSV file at the specified location.

    This function attempts to write the given dataframe to a CSV file.
    The CSV output will include a header and exclude the index.

    :param df: The dataframe to be written to the CSV file.
    :type df: pandas.DataFrame
    :param output_file: The path to the output file where the dataframe will
        be saved as a CSV.
    :type output_file: str
    :return: None
    """
    logger.info("Writing output.")
    try:
        df.to_csv(output_file, header=True, index=False)
    except Exception as e:
        raise UserException(f"Could not write csv output to {output_file}: {e}.") from e


def run_query(input_file, query_file) -> DataFrame:
    """
    Executes a SPARQL query on a knowledge graph defined by the input file.

    This function takes an input file containing a representation of a knowledge
    graph and a SPARQL query file, executes the query on the graph, and returns
    the resulting data as a DataFrame.

    :param input_file: Path to the file containing the knowledge graph data.
    :param query_file: Path to the file containing the SPARQL query.
    :return: A DataFrame containing the results of the executed query.
    :rtype: DataFrame
    """
    query = get_sparql(query_file)
    kg = get_kg(input_file)
    logger.info("Starting query.")
    df = sparql_select(kg, query)
    return df


if __name__ == "__main__":
    try:
        main()
    except UserException as e:
        logger.error(e)
