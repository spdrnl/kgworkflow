import logging
import time

from kgworkflow.util.helper import reason, get_kg, output_ttl, sparql_select, get_sparql

from dotenv import load_dotenv

from kgworkflow.util.setup_logging import setup_logging

# Get settings from .env
load_dotenv()

# Logging
setup_logging()
logger = logging.getLogger(__name__)

def main():

    start_time = time.time()

    logger.info("Read Turtle file.")
    kg = get_kg("src/resources/ttl/zebra.ttl")

    logger.info("Running reasoner.")
    # See robot-test.sh for example robot config, not standard.
    inferred_kg = reason(kg, reasoner="hermit")

    logger.info("Writing results to out.ttl for verification.")
    output_ttl(inferred_kg)

    logger.info("Running SPARQL query.")
    query = get_sparql("src/resources/sparql/zebra.sparql")
    df = sparql_select(inferred_kg, query)

    # Report time
    end_time = time.time()
    logger.info(f"Solved in {end_time - start_time:0.3f} seconds.")

    print(df.to_markdown())

if __name__ == "__main__":
    main()