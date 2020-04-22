import argparse
import json
from typing import AnyStr, List

from DbInterface import Neo4jStream
from TestGraphGenerator import export_database_neo4j, create_graph_map, export_database_json
from TestGraphGenerator.DbTranformations import import_database_json
from TestGraphGenerator.DbTranformations.DbLoader import delete_database_neo4j


def load_names_data_set(path: AnyStr) -> List[AnyStr]:
    """
    Loads a list of names from a json file to use as properties in the test database.
    :param path: the path to the file containing the names
    :return: A list of names if the file is readable else returns none
    """
    with open(path) as data_file:
        data_json = json.load(data_file)
    return data_json['names']


def create_arg_parser() -> argparse.ArgumentParser:
    """
    Creates an arg parser for the script for ease of use as a cli
    :return: the arg parser
    """
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="generate graphs")
    generate_parser = subparsers.add_parser("generate", help="generates a graph from a random names database")
    generate_parser.add_argument("--names", "-n",
                                 help="the path to the file containing the names for the randomly generated nodes")
    generate_parser.add_argument("--output_file", "-o",
                                 help="output file path will output the database as a json",
                                 default="graph.json")
    generate_parser.set_defaults(func=handle_generating)
    neo4j_parser = subparsers.add_parser("neo4j", help="manages database and neo4j bridging")
    neo4j_parser.add_argument("--mode", "-m", choices=["load", "delete"], help="the mode of usage")
    neo4j_parser.add_argument("--username", "-u", help="the neo4j server username")
    neo4j_parser.add_argument("--password", "-p", help="the neo4j server password")
    neo4j_parser.add_argument("--address", "-a", help="the neo4j server address")
    neo4j_parser.add_argument("--database", "--db", help="a database file to load into neo4j", required=False)
    neo4j_parser.set_defaults(func=handle_neo4j)

    return parser


def handle_neo4j(args) -> None:
    """
    Handles the neo4j side of the cli
    :param args: the args from the command line
    """
    with Neo4jStream(args.address, args.username, args.password) as stream:
        if args.mode == "load":
            with open(args.database) as db_file:
                db_json = json.load(db_file)
            database = import_database_json(db_json)
            export_database_neo4j(database, stream)
        elif args.mode == "delete":
            delete_database_neo4j(stream)


def handle_generating(args) -> None:
    """
    Handles generating databases from the cli
    :param args: the args from the command line
    """
    with open(args.output_file, "w+") as output:
        names = load_names_data_set(args.names)
        database = create_graph_map(names)
        database_json = export_database_json(database)
        json.dump(database_json, output)


def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
