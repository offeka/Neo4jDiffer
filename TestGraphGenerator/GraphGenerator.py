from typing import List, AnyStr, Iterable

from DbInterface.Neo4jWriter import Neo4jWriter
from Config import GlobalSettings
import json

from TestGraphGenerator.Models import Node
from TestGraphGenerator.QuerySticher import create_node_query


def create_graph_map():
    names = load_names_data_set(GlobalSettings.NAMES_DATA_SET_PATH)
    nodes = (Node(GlobalSettings.TEST_GRAPH_TYPE, properties={"name": name}) for name in names)
    with Neo4jWriter(GlobalSettings.DB_ADDRESS, GlobalSettings.DB_USERNAME, GlobalSettings.DB_PASSWORD) as writer:
        flush_nodes_to_graph(nodes, writer)


def load_names_data_set(path: AnyStr) -> List:
    with open(path) as data_file:
        data_json = json.load(data_file)
    return data_json['names']


def flush_nodes_to_graph(nodes: Iterable[Node], writer: Neo4jWriter) -> None:
    for node in nodes:
        query = create_node_query(node)
        writer.write(query)


create_graph_map()
