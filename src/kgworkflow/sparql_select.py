import argparse
import logging
import os
import time

from dotenv import load_dotenv
from pandas import DataFrame

from kgworkflow.util.helper import get_sparql, sparql_select, get_kg
from kgworkflow.util.setup_logging import setup_logging

# Get settings from .env
load_dotenv()

# Logging
setup_logging()
logger = logging.getLogger(__name__)

def get_args() -> argparse.Namespace:
    # Initialize
    parser = argparse.ArgumentParser(
        description='The program executes a SPARQL query file against a Turtle file and outputs the results as CSV.',
        epilog='Happy querying!',
        prog="sparql-select")

    # Adding optional parameters
    parser.add_argument('-q',
                        '--query-file',
                        help="SPARQL query file.",
                        required=True,
                        type=str)

    parser.add_argument('-i',
                        '--input-file',
                        help="Turtle input file.",
                        required=True,
                        type=str)

    parser.add_argument('-o',
                        '--output-file',
                        help="Csv output file.",
                        required=True,
                        type=str)

    return parser.parse_args()


def main():
    # Resolve the arguments
    args = get_args()
    query_file = args.query_file
    input_file = args.input_file
    output_file = args.output_file

    # Echo settings
    logger.info(f"Query file: {query_file}")
    logger.info(f"Input file: {input_file}")
    logger.info(f"Output file: {output_file}")

    # Check if files exist
    if not os.path.exists(query_file):
        logger.error(f"Query file {query_file} does not exist.")

    if not os.path.exists(input_file):
        logger.error(f"Input file {input_file} does not exist.")

    # Execute the query
    start_time = time.time()

    df = run_query(input_file, query_file)
    write_output(df, output_file)

    end_time = time.time()
    logger.info(f"Done in {end_time - start_time:0.3f} seconds.")


def write_output(df, output_file):
    logger.info(f"Writing output.")
    try:
        df.to_csv(output_file, header=True, index=False)
    except Exception as e:
        logger.error(f"Could not write output to {output_file}: {e}.")


def run_query(input_file, query_file) -> DataFrame:
    query = get_sparql(query_file)
    kg = get_kg(input_file)
    logger.info(f"Starting query.")
    df = sparql_select(kg, query)
    return df


if __name__ == "__main__":
    main()
