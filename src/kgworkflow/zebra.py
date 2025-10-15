import logging
import time

from kgworkflow.helpers.general_helper import (
    UserException,
)
from kgworkflow.helpers.ttl_helper import output_ttl, read_ttl_kg
from kgworkflow.helpers.reasoner_helper import infer_graph
from kgworkflow.helpers.sparql_helper import sparql_select, read_sparql

from dotenv import load_dotenv

from kgworkflow.logging.setup_logging import setup_logging

# Get settings from .env
load_dotenv()

# Logging
setup_logging()
logger = logging.getLogger(__name__)


def main():
    start_time = time.time()

    logger.info("Read Turtle file.")
    kg = read_ttl_kg("input/ttl/zebra.ttl")

    logger.info("Running reasoner.")
    # See robot-test.sh for example robot config, not standard.
    inferred_kg = infer_graph(kg, reasoner="hermit")

    logger.info("Writing results to out.ttl for verification.")
    output_ttl(inferred_kg)

    logger.info("Running SPARQL query.")
    query = read_sparql("input/sparql/zebra.sparql")
    df = sparql_select(inferred_kg, query)

    # Report time
    end_time = time.time()
    logger.info(f"Solved in {end_time - start_time:0.3f} seconds.")

    print(df.to_markdown())


if __name__ == "__main__":
    try:
        main()
    except UserException as e:
        logger.error(e)
