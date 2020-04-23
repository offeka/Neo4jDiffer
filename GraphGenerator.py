import argparse
import json
from typing import AnyStr, List

from DatabaseGenerator.DatabaseGenerator import create_graph_map
from GraphModeler import export_database_json


def load_names_data_set(path: AnyStr) -> List[AnyStr]:
    """
    Loads a list of names from a json file to use as properties in the test database.
    :param path: the path to the file containing the names
    :return: A list of names if the file is readable else returns none
    """
    with open(path) as data_file:
        try:
            data_json = json.load(data_file)
        except json.JSONDecodeError:
            print("Invalid names file make sure you are using the correct format and file")
    return data_json['names']


def create_arg_parser() -> argparse.ArgumentParser:
    """
    Creates an arg parser for the script for ease of use as a cli
    :return: the arg parser
    """
    generate_parser = argparse.ArgumentParser()
    generate_parser.add_argument("--names", "-n",
                                 help="the path to the file containing the names for the randomly generated nodes")
    generate_parser.add_argument("--output_file", "-o",
                                 help="output file path will output the database as a json",
                                 default="graph.json")
    generate_parser.add_argument("--connection_chance", "-c",
                                 help="the chance for a node to connect to another one, higher is a bigger chance",
                                 default=5,
                                 type=int)
    generate_parser.set_defaults(func=generation_command)

    return generate_parser


def generation_command(args) -> None:
    """
    Handles generating databases from the cli
    :param args: the args from the command line
    """
    with open(args.output_file, "w+") as output:
        names = load_names_data_set(args.names)
        database = create_graph_map(names, args.connection_chance)
        database_json = export_database_json(database)
        json.dump(database_json, output)


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
