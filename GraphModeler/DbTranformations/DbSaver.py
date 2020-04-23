from typing import Dict, Iterable

from tqdm import tqdm

from DbInterface import Neo4jStream
from GraphModeler.DbTranformations.QuerySticher import create_node_query, create_relationship_query

from GraphModeler.Models import Node, Relationship
from GraphModeler.Models.Database import Database
from GraphModeler.Models.Graph import Graph


def export_node_json(node: Node) -> Dict:
    """
    Converts a node to json for serialization
    :param node: the node to convert
    :return: a dict representing the node
    """
    return {"node_types": node.node_types, "properties": node.properties}


def export_relationship_json(rel: Relationship) -> Dict:
    """
    Converts a relationship to json using the nodes ids
    :param rel: the relationship to convert
    :return: a dict representing the relationship
    """
    return {"node_a": rel.node_a.node_id, "relationship_type": rel.relationship_type, "node_b": rel.node_b.node_id,
            "properties": rel.properties}


def export_graph_json(graph: Graph) -> Dict:
    """
    Converts a graph to json
    :param graph: the graph to serialize
    :return: a dict representing the graph
    """
    return {"nodes": [export_node_json(node) for node in graph.nodes],
            "relationships": [export_relationship_json(rel) for rel in graph.relationships]}


def export_database_json(database: Database) -> Dict:
    """
    Converts a database to json for saving and loading.
    This is not a replacement for neo4j dump feature this is used in context of a single db.
    For example to use :dbs in neo4j and load different ones in the same instance.
    :param database:
    :return: a dict representing the database
    """
    return {"name": database.name, "graph": export_graph_json(database.graph)}


def export_database_neo4j(database: Database, stream: Neo4jStream) -> None:
    """
    Loads a database from an object into neo4j
    :param database: the database to load
    :param stream: the neo4j interface to use
    """
    export_nodes_to_graph(database.graph.nodes, stream)
    export_relationships_to_graph(database.graph.relationships, stream)


def export_nodes_to_graph(nodes: Iterable[Node], stream: Neo4jStream) -> None:
    """
    Creates a list of nodes in the neo4j graph.
    :param nodes: the nodes to create in the db
    :param stream: a neo4j interface to send queries to
    """
    for node in tqdm(nodes, "nodes sent to neo4j"):
        stream.write(create_node_query(node))


def export_relationships_to_graph(relationships: Iterable[Relationship], stream: Neo4jStream) -> None:
    """
    Writes relationships to the neo4j database.
    :param relationships: the relationships to create in the db
    :param stream: a neo4j interface to send queries to
    """
    for relationship in tqdm(relationships, "relationships sent to neo4j"):
        stream.write(create_relationship_query(relationship))


def delete_database_neo4j(stream: Neo4jStream):
    """
    Deletes a neo4j database
    WARNING! THIS WILL DELETE THE DATABASE IN NEO4J PERMANENTLY
    :param stream:
    :return:
    """
    stream.write("MATCH (n) DETACH DELETE n")
