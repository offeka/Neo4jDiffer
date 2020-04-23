from typing import Callable

from Config import GlobalSettings
from GraphModeler.Models import Relationship, Node
from GraphModeler.Models.Database import Database
from copy import deepcopy
import random


def perturb_graph(database: Database, perturb_chance: float, iterations: int) -> Database:
    """
    Takes a database and changes it small changes for testing differences between graphs
    WARNING! This function will copy the whole database in memory, should not be used if you care about your ram usage
    :param database: the database to change
    :param perturb_chance: the chance of a node changing or a relationship changing
    :param iterations: the amount of iterations to run over the graph
    :return: a new database slightly changed
    """
    db_copy = deepcopy(database)
    perturb_graph_reference(db_copy, perturb_chance, iterations)
    return db_copy


def perturb_graph_reference(database: Database, perturb_chance: float, iterations: int) -> None:
    """
    Takes a database and changes it small changes for testing differences between graphs
    WARNING! this function modifies the sent graph
    :param database: the database to modify
    :param perturb_chance: the chance of a node or a relationship changing
    :param iterations: the amount of iterations to run over the graph to perturb
    """
    for action in [delete_random_node, create_random_relationship, delete_random_relationship]:
        for i in range(iterations):
            if perturb_chance > random.random():
                action(database)


def create_random_relationship(database: Database) -> None:
    """
    add a random relationship in the graph
    :param database: the database to modify
    """
    node_a = random.choice(database.graph.nodes)
    node_b = random.choice(database.graph.nodes)
    rel = Relationship(node_a, GlobalSettings.TEST_GRAPH_RELATIONSHIP, node_b)
    database.graph.relationships.append(rel)


def delete_random_node(database: Database) -> None:
    """
    Removes a random node from the graph
    :param database: the database to remove the node from
    """
    selected_node = random.choice(database.graph.nodes)
    detach_node(database, selected_node)
    database.graph.nodes.remove(selected_node)


def detach_node(database: Database, node: Node) -> None:
    """
    Removes all of the nodes relationships
    :param database: the database to remove the relationships from
    :param node: the node to detach
    """
    node_relationships = filter(lambda rel: rel.node_a == node or rel.node_b == node, database.graph.relationships)
    database.graph.relationships = list(set(database.graph.relationships) - set(node_relationships))


def delete_random_relationship(database: Database) -> None:
    """
    Removes a random node from the graph
    :param database: the database to remove the node from
    """
    database.graph.relationships.remove(random.choice(database.graph.relationships))
