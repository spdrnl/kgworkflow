import argparse

from util.kg import get_sparql, sparql_select, get_kg


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

    # Execute the query
    query = get_sparql(query_file)
    kg = get_kg(input_file)
    result = sparql_select(kg, query)
    result.to_csv(output_file, header=True, index=False)


if __name__ == "__main__":
    main()
