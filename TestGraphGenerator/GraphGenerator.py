import json
import random
from typing import List, AnyStr, Optional

from Config import GlobalSettings
from TestGraphGenerator.Models import Node, Relationship
from TestGraphGenerator.Models.Database import Database
from TestGraphGenerator.Models.Graph import Graph


def create_graph_map(path: AnyStr) -> Database:
    """
    Creates a randomly generated graph in neo4j and saves it to a json representation for use in testing the differ
    loads names for generating from a file.
    :param path: the path to save the graph to.
    """
    names = load_names_data_set(path)
    relationships = []
    names_nodes = [Node(GlobalSettings.TEST_GRAPH_TYPE, properties={"name": name}) for name in names]
    for current_node in names_nodes:
        for i in range(random.randint(1, 5)):
            selected_node = random.choice(names_nodes)
            if selected_node is not current_node:
                new_relationship = Relationship(current_node, "KNOWS", selected_node)
                relationships.append(new_relationship)
    return Database(Graph(names_nodes, relationships), "TestDatabase")


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