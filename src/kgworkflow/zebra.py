import logging

from kgworkflow.util.helper import reason, get_kg, output_ttl, sparql_select, get_sparql

from dotenv import load_dotenv

from kgworkflow.util.setup_logging import setup_logging

# Get settings from .env
load_dotenv()

# Logging
setup_logging()
logger = logging.getLogger(__name__)

def main():
    # See robot-test.sh for the robot config, not standard.
    logger.info("Read Turtle file.")
    kg = get_kg("src/resources/ttl/zebra.ttl")

    logger.info("Running reasoner.")
    inferred_kg = reason(kg, reasoner="hermit")

    logger.info("Writing results to out.ttl for verification.")
    output_ttl(inferred_kg)

    logger.info("Running SPARQL query.")
    query = get_sparql("src/resources/sparql/zebra.sparql")
    df = sparql_select(inferred_kg, query)
    print(df)

if __name__ == "__main__":
    main()