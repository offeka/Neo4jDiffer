import argparse
import json
from typing import AnyStr, List


def load_names_data_set(path: AnyStr) -> List[AnyStr]:
    """
    Loads a list of names from a json file to use as properties in the test database.
    :param path: the path to the file containing the names
    :return: A list of names if the file is readable else returns none
    """
    with open(path) as data_file:
        data_json = json.load(data_file)
    return data_json['names']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--names", "-n",
                        help="the path to the file containing the names for the randomly generated nodes",
                        required=False)
    parser.add_argument("--output_file", "-o",
                        help="output file path will output the database as a json",
                        required=False)
    parser.add_argument("--neo4j", "-j", help="whether to output to neo4j, cannot be used with file output",
                        required=False)
    parser.add_argument("--database", "--db", help="a database file to load into neo4j", required=False)
    parser.add_argument("--username", "-u", help="the neo4j server username", required=False)
    parser.add_argument("--password", "-p", help="the neo4j server password", required=False)
    parser.add_argument("--address", "-a", help="the neo4j server address", required=False)
    parser.parse_args()


main()
