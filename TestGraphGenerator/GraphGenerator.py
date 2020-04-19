from typing import List, AnyStr, Iterable, Optional

from DbInterface.Neo4jWriter import Neo4jWriter
from Config import GlobalSettings
import json

from TestGraphGenerator.Models import Node
from TestGraphGenerator.QuerySticher import create_node_query, delete_node_query


def create_graph_map(path: AnyStr):
    """
    Creates a randomly generated graph in neo4j and saves it to a json representation for use in testing the differ
    loads names for generating from a file.
    :param path: the path to save the graph to.
    """
    names = load_names_data_set(GlobalSettings.NAMES_DATA_SET_PATH)
    if names:
        names_nodes = [Node(GlobalSettings.TEST_GRAPH_TYPE, properties={"name": name}) for name in names]
        with Neo4jWriter(GlobalSettings.DB_ADDRESS, GlobalSettings.DB_USERNAME, GlobalSettings.DB_PASSWORD) as writer:
            flush_nodes_to_graph(names_nodes, writer)
            deletes = [writer.write(delete_node_query(node)) for node in names_nodes]


def load_names_data_set(path: AnyStr) -> Optional[List]:
    """
    Loads a list of names from a json file to use as properties in the test database.
    :param path: the path to the file containing the names
    :return: A list of names if the file is readable else returns none
    """
    try:
        with open(path) as data_file:
            data_json = json.load(data_file)
    except IOError:
        return None
    return data_json['names']


def flush_nodes_to_graph(nodes: Iterable[Node], writer: Neo4jWriter) -> None:
    """
    Creates a list of nodes in the neo4j graph.
    You might ask yourself why is this a function and not a list comp?
    it is more readable and doesnt return anything meaningful so a list comp is hack at best
    :param nodes: the nodes to create in the db
    :param writer: a neo4j interface to send queries
    """
    for node in nodes:
        writer.write(create_node_query(node))


create_graph_map()
