from typing import Dict

from TestGraphGenerator.Models import Node, Relationship
from TestGraphGenerator.Models.Database import Database
from TestGraphGenerator.Models.Graph import Graph


def node_json(node: Node) -> Dict:
    """
    Converts a node to json for serialization
    :param node: the node to convert
    :return: a dict representing the node
    """
    return {"node_type": node.node_type, "properties": node.properties}


def relationship_json(rel: Relationship) -> Dict:
    """
    Converts a relationship to json using the nodes ids
    :param rel: the relationship to convert
    :return: a dict representing the relationship
    """
    return {"node_a": rel.node_a.node_id, "relationship_type": rel.relationship_type, "node_b": rel.node_b.node_id}


def graph_json(graph: Graph) -> Dict:
    """
    Converts a graph to json
    :param graph: the graph to serialize
    :return: a dict representing the graph
    """
    return {"nodes": [node_json(node) for node in graph.nodes],
            "relationships": [relationship_json(rel) for rel in graph.relationships]}


def database_json(database: Database) -> Dict:
    """
    Converts a database to json for saving and loading.
    This is not a replacement for neo4j dump feature this is used in context of a single db.
    For example to use :dbs in neo4j and load different ones in the same instance.
    :param database:
    :return: a dict representing the database
    """
    return {"name": database.name, "graph": graph_json(database.graph)}
