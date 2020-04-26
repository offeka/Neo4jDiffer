import asyncio
from typing import Dict, Iterable

from tqdm import tqdm

from DbInterface import Neo4jStream
from DbInterface.Neo4jStreamAsync import Neo4jStreamAsync
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
    for node in nodes:
        stream.write(create_node_query(node))


async def export_nodes_to_graph_async(nodes: Iterable[Node], stream: Neo4jStreamAsync) -> None:
    """
    Creates a list of nodes in neo4j in an async manner
    :param nodes: the nodes to export
    :param stream: the neo4j stream to write to
    """
    await asyncio.wait([stream.write_async(create_node_query(node)) for node in nodes])


def export_relationships_to_graph(relationships: Iterable[Relationship], stream: Neo4jStream) -> None:
    """
    Writes relationships to the neo4j database.
    :param relationships: the relationships to create in the db
    :param stream: a neo4j interface to send queries to
    """
    for relationship in relationships:
        stream.write(create_relationship_query(relationship))


async def export_relationships_to_graph_async(relationships: Iterable[Relationship], stream: Neo4jStreamAsync) -> None:
    """
    Exports relationships to neo4j graph in an async manner
    :param relationships: the relationships to export
    :param stream: the stream to write
    """
    await asyncio.wait([stream.write_async(create_relationship_query(rel)) for rel in relationships])


def delete_database_neo4j(stream: Neo4jStream):
    """
    Deletes a neo4j database
    WARNING! THIS WILL DELETE THE DATABASE IN NEO4J PERMANENTLY
    :param stream:
    :return:
    """
    stream.write("MATCH (n) DETACH DELETE n")


async def delete_database_neo4j_async(stream: Neo4jStreamAsync) -> None:
    """
    Deletes a neo4j database in an async manner
    WARNING! THIS WILL DELETE THE NEO4J CONTENTS PERMANENTLY
    :param stream: the stream to delete the database from
    """
    await stream.write_async("MATCH (n) DETACH DELETE n")
