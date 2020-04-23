import argparse
import json

from DbInterface import Neo4jStream
from GraphModeler import export_database_neo4j
from GraphModeler.DbTranformations import import_database_json
from GraphModeler.DbTranformations.DbLoader import delete_database_neo4j


def create_arg_parser() -> argparse.ArgumentParser:
    neo4j_parser = argparse.ArgumentParser()
    neo4j_parser.add_argument("--mode", "-m", choices=["load", "delete"], help="the mode of usage")
    neo4j_parser.add_argument("--username", "-u", help="the neo4j server username")
    neo4j_parser.add_argument("--password", "-p", help="the neo4j server password")
    neo4j_parser.add_argument("--address", "-a", help="the neo4j server address")
    neo4j_parser.add_argument("--database", "-d", help="a database file to load into neo4j", required=False)
    neo4j_parser.set_defaults(func=neo4j_command)
    return neo4j_parser


def neo4j_command(args) -> None:
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


def run():
    parser = create_arg_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    run()
