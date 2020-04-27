import argparse
import json
from typing import AnyStr, List

from DatabaseGenerator.DatabaseGenerator import create_graph_map
from GraphModeler import export_database_json, import_database_json
from GraphModeler.DbTranformations.DbPerturber import perturb_graph_reference


def load_names_data_set(path: AnyStr) -> List[AnyStr]:
    """
    Loads a list of names from a json file to use as properties in the test database.
    :param path: the path to the file containing the names
    :return: A list of names if the file is readable else returns none
    """
    with open(path, encoding="UTF-8") as data_file:
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
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    perturb_parser = subparsers.add_parser("perturb")
    perturb_parser.add_argument("--database", "-d", help="the database json file to perturb")
    perturb_parser.add_argument("--output", "-o", help="the output file for the new perturb database")
    perturb_parser.add_argument("--perturb_chance", "-c", help="the chance for the graph to mutate", type=float)
    perturb_parser.add_argument("--iterations", "-i", help="the amount of times to go over the graph and mutate it",
                                type=int)
    perturb_parser.set_defaults(func=perturb_command)
    generate_parser = subparsers.add_parser("generate")
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

    return parser


def generation_command(args) -> None:
    """
    Handles generating databases from the cli
    :param args: the args from the command line
    """
    try:
        with open(args.output_file, "w+") as output:
            names = load_names_data_set(args.names)
            database = create_graph_map(names, args.connection_chance)
            database_json = export_database_json(database)
            json.dump(database_json, output)
    except FileExistsError:
        print("File already exists. please choose a different filename")


def perturb_command(args) -> None:
    try:
        with open(args.database, "r") as db_file:
            db_json = json.load(db_file)
            database = import_database_json(db_json)
            perturb_graph_reference(database, args.perturb_chance, args.iterations)
        with open(args.output, "w+") as output_file:
            json.dump(export_database_json(database), output_file)
    except FileExistsError:
        print("File already exists please choose a different filename")
    except FileNotFoundError:
        print("File not found please make sure you entered the correct file path")
    except json.JSONDecodeError:
        print("Invalid database file")


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
