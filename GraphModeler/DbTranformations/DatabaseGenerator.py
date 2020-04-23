import random
from typing import List, AnyStr

from Config import GlobalSettings
from GraphModeler.Models import Node, Relationship
from GraphModeler.Models.Database import Database
from GraphModeler.Models.Graph import Graph


def create_graph_map(names: List[AnyStr], connection_chance: int) -> Database:
    """
    Creates a randomly generated graph in neo4j and saves it to a json representation for use in testing the differ
    loads names for generating from a file.
    :param connection_chance: the chance for a node to connect to another higher is a bigger change
    :param names: the path to save the graph to.
    """
    names = names
    relationships = []
    names_nodes = [Node(GlobalSettings.TEST_GRAPH_TYPE, properties={"name": name}) for name in names]
    for current_node in names_nodes:
        for i in range(random.randint(connection_chance)):
            selected_node = random.choice(names_nodes)
            if selected_node is not current_node:
                new_relationship = Relationship(current_node, "KNOWS", selected_node)
                relationships.append(new_relationship)
    return Database(Graph(names_nodes, relationships), "TestDatabase")
